from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType
import numpy
import dlib
import cv2
import time
import math


class StaticMovementDetector:
    def __init__(
        self,
        cameraObject: Camera,
        noiseMargin: int = 50,
        movementThreshold: float = 3,
        movementTimeout: int = 5000,
        showFrame: bool = False,
    ):
        super().__init__()

        self.camera = cameraObject
        self.orb = cv2.ORB_create()
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        self.showFrame = showFrame

        if self.showFrame == True:
            self.imageWindow = dlib.image_window()

        self.noiseMargin = noiseMargin
        self.movementThreshold = movementThreshold
        self.movementTimeout = movementTimeout

        self.previousImage = None
        self.currentImage = None

        self.staticStartTime = None
        self.isStart = True

    def compareFrame(self) -> bool:
        if self.isStart:

            self.currentImage = self.camera.takeFrame()
            self.isStart = False

            return False

        else:

            self.previousImage = self.currentImage
            self.currentImage = self.camera.takeFrame()

            kp1, des1 = self.orb.detectAndCompute(self.previousImage, None)
            kp2, des2 = self.orb.detectAndCompute(self.currentImage, None)

            if des2 is None:
                des2 = []
            matches = self.bf.match(des1, des2)

            matches = sorted(matches, key=lambda x: x.distance)

            dmatchDistanceList = []
            realDistanceList = []

            if self.showFrame == True:
                outputImage = self.currentImage

            for match in matches:

                image1KeypointId = match.queryIdx
                image2KeypointId = match.trainIdx

                image1Keypoint = kp1[image1KeypointId]
                image2Keypoint = kp2[image2KeypointId]

                image1Coordinate = image1Keypoint.pt
                image2Coordinate = image2Keypoint.pt

                xDiff = abs(image1Coordinate[0] - image2Coordinate[0])
                yDiff = abs(image1Coordinate[1] - image2Coordinate[1])

                dist = math.sqrt((xDiff * xDiff) + (yDiff * yDiff))

                if dist > self.noiseMargin:
                    continue

                dmatchDistanceList.append(match.distance)
                realDistanceList.append(dist)

                if self.showFrame == True:

                    cv2.line(
                        outputImage,
                        (int(image1Coordinate[0]), int(image1Coordinate[1])),
                        (int(image2Coordinate[0]), int(image2Coordinate[1])),
                        (0, 255, 0),
                        1,
                    )

            if self.showFrame == True:
                self.imageWindow.clear_overlay()
                self.imageWindow.set_image(outputImage)

            # print("Average: {}".format(numpy.average(realDistanceList)))

            if numpy.average(realDistanceList) < self.movementThreshold:
                return True
            else:
                return False

    def detectStatic(self):

        isStatic = self.compareFrame()
        # print("FrameStatic: {}".format(isStatic))

        if self.staticStartTime == None:
            self.staticStartTime = time.time() * 1000
            return False

        else:
            currentTime = time.time() * 1000

            if isStatic == True:
                if (currentTime - self.staticStartTime) > self.movementTimeout:
                    return True
                else:
                    return False
            else:
                self.staticStartTime = currentTime
                return False
