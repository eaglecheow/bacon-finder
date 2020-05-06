from typing import List
import os
import dlib
import numpy
from imutils import face_utils
import time

from raspi.utils.datapresentation.GraphPlotter import GraphPlotter

from raspi.utils.dataprocess.DataObserver import DataObserver


class EyelidDetector:
    def __init__(
        self,
        predictionFilePath: str,
        faceAbsenceTimeout: int = 100000,
        eyelidMovementTimeout: int = 30000,
        frameTimeTimeout: int = 1000,
        eyelidMovementThreshold: float = 0.025,
        showFrame: bool = False,
    ):
        super().__init__()

        if not os.path.exists(predictionFilePath):
            raise FileNotFoundError(predictionFilePath)

        faceDetector = dlib.get_frontal_face_detector()
        faceFeatureDetector = dlib.shape_predictor(predictionFilePath)

        self.faceDetector = faceDetector
        self.faceFeatureDetector = faceFeatureDetector
        self.dataProcessor = DataObserver()

        self.faceAbsenceTimeout = faceAbsenceTimeout
        self.eyelidMovementTimeout = eyelidMovementTimeout
        self.frameTimeTimeout = frameTimeTimeout
        self.eyelidMovementThreshold = eyelidMovementThreshold
        self.showFrame = showFrame

        self.isIdle = False
        self.accumulatedIdleTime = 0

        self.lastScanTime = time.time() * 1000
        self.lastFacePresenceTime = time.time() * 1000
        self.lastEyelidMoveTime = time.time() * 1000

        if self.showFrame:
            self.imageWindow = dlib.image_window()
            self.imageWindow.set_title("Face Detector")
            self.graphPlotter = GraphPlotter()
            self.graphPlotter.add_plot("ear", "Eye Aspect Ratio")
            self.graphPlotter.add_plot("variance", "Variance x25")
            self.graphPlotter.show_graph()

    def frameDetection(self, frame) -> bool:
        currentTime = time.time() * 1000

        if (currentTime - self.lastScanTime) > self.frameTimeTimeout:
            raise Exception("[Face Detector] Each frame took too much time")

        self.lastScanTime = currentTime

        detectedFaceList = self.faceDetector(frame)

        if self.showFrame:
            self.imageWindow.clear_overlay()
            self.imageWindow.set_image(frame)

        if len(detectedFaceList) <= 0:

            if (currentTime - self.lastFacePresenceTime) > self.faceAbsenceTimeout:
                # return {'resultType': 'eyelid', 'result': False}
                return False

            # return {'resultType': 'eyelid', 'result': True}
            return True

        self.lastFacePresenceTime = currentTime

        maxFaceArea = 0
        selectedFace = None

        for faceIndex, faceBoundingBox in enumerate(detectedFaceList):

            xDiff = abs(faceBoundingBox.right() - faceBoundingBox.left())
            yDiff = abs(faceBoundingBox.bottom() - faceBoundingBox.top())
            faceArea = xDiff * yDiff

            if faceArea > maxFaceArea:
                maxFaceArea = faceArea
                selectedFace = faceBoundingBox

        faceFeatures = self.faceFeatureDetector(frame, selectedFace)

        if self.showFrame:
            self.imageWindow.add_overlay(selectedFace)
            self.imageWindow.add_overlay(faceFeatures)

        faceFeaturePoints = face_utils.shape_to_np(faceFeatures)
        (leftEyeStartIndex, leftEyeEndIndex) = face_utils.FACIAL_LANDMARKS_IDXS[
            "left_eye"
        ]
        (rightEyeStartIndex, rightEyeEndIndex) = face_utils.FACIAL_LANDMARKS_IDXS[
            "right_eye"
        ]

        leftEyePoints = faceFeaturePoints[leftEyeStartIndex:leftEyeEndIndex]
        rightEyePoints = faceFeaturePoints[rightEyeStartIndex:rightEyeEndIndex]

        leftEAR = self.__eye_aspect_ratio__(leftEyePoints)
        rightEAR = self.__eye_aspect_ratio__(rightEyePoints)
        averageEAR = (leftEAR + rightEAR) / 2.0

        self.dataProcessor.inputValue(averageEAR)
        variance25 = self.dataProcessor.varValue * 25

        if variance25 > self.eyelidMovementThreshold:
            self.lastEyelidMoveTime = currentTime

        if self.showFrame:
            self.graphPlotter.input_value("ear", averageEAR)
            self.graphPlotter.input_value("variance", variance25)

        # print("Eyelid idle time: {} ms".format(currentTime - self.lastEyelidMoveTime))

        if (currentTime - self.lastEyelidMoveTime) > self.eyelidMovementTimeout:
            # return {'resultType': 'eyelid', 'result': False}
            return False

        # return {'resultType': 'eyelid', 'result': True}
        return True

    def __euclidean_distance__(self, pointA: float, pointB: float) -> float:

        return numpy.linalg.norm(pointA - pointB)

    def __eye_aspect_ratio__(self, eye: List[float]) -> float:

        A = self.__euclidean_distance__(eye[1], eye[5])
        B = self.__euclidean_distance__(eye[2], eye[4])

        C = self.__euclidean_distance__(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)

        return ear
