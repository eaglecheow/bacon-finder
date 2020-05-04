import os
import dlib
import time

from imutils import face_utils
from raspi.utils.dataprocess.DataObserver import DataObserver
import numpy
from typing import List

class EyelidDetector:
    def __init__(
        self,
        faceModelFilePath: str,
        faceAbsenceTimeout: int = 100000,
        eyelidMovementTimeout: int = 30000,
        frameTimeTimeout: int = 1000,
        eyelidMovementThreshold: float = 0.025,
        showFrame: bool = False,
    ):
        super().__init__()

        # Check if face model is available
        if not os.path.exists(faceModelFilePath):
            raise FileNotFoundError(faceModelFilePath)

        faceDetector = dlib.get_frontal_face_detector()
        faceFeatureDetector = dlib.shape_predictor(faceModelFilePath)

        self.faceDetector = faceDetector
        self.faceFeatureDetector = faceFeatureDetector
        self.dataProcessor = DataObserver()

        self.eyelidMovementThreshold = eyelidMovementThreshold
        self.eyelidMovementTimeout = eyelidMovementTimeout

        self.previousIdleTime = int(time.time() * 1000)

    def frameDetection(self, frame) -> bool:

        currentTime = int(time.time() * 1000)

        detectedFaceList = self.faceDetector(frame)
        if len(detectedFaceList) < 1:
            # No face detected

            self.previousIdleTime = currentTime

            return False

        # Determining which face is the nearest to camera
        maxFaceArea = 0
        selectedFace = None
        for faceIndex, faceBoundingBox in enumerate(detectedFaceList):
            xDiff = abs(faceBoundingBox.right() - faceBoundingBox.left())
            yDiff = abs(faceBoundingBox.bottom() - faceBoundingBox.top())
            faceArea = xDiff * yDiff

            if faceArea > maxFaceArea:
                maxFaceArea = faceArea
                selectedFace = faceBoundingBox

        # Extracting eyelid info from selected face
        faceFeatures = self.faceFeatureDetector(frame, selectedFace)
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

        # Process eyelid data along with previous record
        self.dataProcessor.inputValue(averageEAR)
        variance25 = self.dataProcessor.varValue * 25

        if variance25 > self.eyelidMovementThreshold:
            self.previousIdleTime = currentTime

        if (currentTime - self.previousIdleTime) > self.eyelidMovementTimeout:
            return True

        return False

    def __euclidean_distance__(self, pointA: float, pointB: float) -> float:

        return numpy.linalg.norm(pointA - pointB)

    def __eye_aspect_ratio__(self, eye: List[float]) -> float:

        A = self.__euclidean_distance__(eye[1], eye[5])
        B = self.__euclidean_distance__(eye[2], eye[4])

        C = self.__euclidean_distance__(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)

        return ear
