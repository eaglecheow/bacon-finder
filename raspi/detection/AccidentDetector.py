from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType
from raspi.detection.camera.EyelidDetector import EyelidDetector
from raspi.detection.camera.StaticMovementDetector import StaticMovementDetector
from raspi.utils.SerialHelper import SerialHelper
from raspi.utils.dataprocess.DataObserver import DataObserver
from raspi.detection.sensor.acceleration.AccelerometerDetector import (
    AccelerometerDetector,
)

import re
import math


class SensorBasedDetector:
    def __init__(self, config):
        super().__init__()

        self.dataObserver = DataObserver()

        generalConfig = config["generalConfig"]
        accConfig = config["accelerometerDetectionConfig"]

        self.serialReader = SerialHelper(
            generalConfig["arduinoSerialPort"], generalConfig["arduinoBaudRate"]
        )

        self.accDetector = AccelerometerDetector(accConfig)

    def readValue(self):
        return self.serialReader.readLine()

    def detect(self) -> bool:

        rawData = self.readValue()
        sensorValuePattern = r"\[\d+\]X:\d+;Y:\d+;Z:\d+;V:\d+;"
        foundPattern = re.findall(sensorValuePattern, rawData)
        if len(foundPattern) >= 1:
            content = foundPattern[0]

            xPattern = r"X:\d+;"
            yPattern = r"Y:\d+;"
            zPattern = r"Z:\d+;"
            vPattern = r"V:\d+;"

            foundX: str = re.findall(xPattern, content)[0]
            foundY = re.findall(yPattern, content)[0]
            foundZ = re.findall(zPattern, content)[0]
            foundV = re.findall(vPattern, content)[0]

            x = int(foundX.replace("X:", "").replace(";", ""))
            y = int(foundY.replace("Y:", "").replace(";", ""))
            z = int(foundZ.replace("Z:", "").replace(";", ""))
            v = int(foundV.replace("V:", "").replace(";", ""))

            accDetection = self.accDetector.detect(x, y, z)
            return accDetection

        return False


class ImageBasedDetector:
    def __init__(
        self, cameraType: CameraType, config, cameraConfig, debug: bool = False
    ):
        super().__init__()

        eyelidDetectorConfig = config["eyelidDetectionConfig"]
        staticMovementConfig = config["staticMovementDetectionConfig"]

        self.camera = Camera(cameraType, cameraConfig)
        self.eyelidDetector = EyelidDetector(
            eyelidDetectorConfig["faceModelFilePath"],
            eyelidDetectorConfig["faceAbsenceTimeout"],
            eyelidDetectorConfig["eyelidMovementTimeout"],
            eyelidDetectorConfig["frameTimeTimeout"],
            eyelidDetectorConfig["eyelidMovementThreshold"],
            showFrame=debug,
        )
        self.staticMovementDetector = StaticMovementDetector(
            staticMovementConfig["noiseMargin"],
            staticMovementConfig["movementThreshold"],
            staticMovementConfig["movementTimeout"],
            showFrame=debug,
        )

    def detect(self) -> bool:

        frame = self.camera.takeFrame()

        isEyelidActive = self.eyelidDetector.frameDetection(frame)
        isImageStatic = self.staticMovementDetector.detectStatic(frame)

        print(
            "isEyelidActive: {} \tisImageStatic: {}".format(
                isEyelidActive, isImageStatic
            )
        )

        return (not isEyelidActive) or isImageStatic

