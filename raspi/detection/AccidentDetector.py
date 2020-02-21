from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType
from raspi.detection.camera.EyelidDetector import EyelidDetector
from raspi.detection.camera.StaticMovementDetector import StaticMovementDetector
from raspi.utils.SerialHelper import SerialHelper


class SensorBasedDetector:
    def __init__(self, config):
        super().__init__()

        generalConfig = config["generalConfig"]

        self.serialReader = SerialHelper(
            generalConfig["arduinoSerialPort"], generalConfig["arduinoBaudRate"]
        )

    def readValue(self):
        return self.serialReader.readLine()


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

