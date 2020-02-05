from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType
from raspi.detection.camera.EyelidDetector import EyelidDetector
from raspi.detection.camera.StaticMovementDetector import StaticMovementDetector


class ImageBasedDetector:
    def __init__(self, cameraType: CameraType, config, debug: bool = False):
        super().__init__()

        eyelidDetectorConfig = config["eyelidDetectionConfig"]
        staticMovementConfig = config["staticMovementDetectionConfig"]

        self.camera = Camera(cameraType)
        self.eyelidDetector = EyelidDetector(
            eyelidDetectorConfig["faceModelFilePath"],
            self.camera,
            eyelidDetectorConfig["faceAbsenceTimeout"],
            eyelidDetectorConfig["eyelidMovementTimeout"],
            eyelidDetectorConfig["frameTimeTimeout"],
            eyelidDetectorConfig["eyelidMovementThreshold"],
            showFrame=debug,
        )
        self.staticMovementDetector = StaticMovementDetector(
            self.camera,
            staticMovementConfig["noiseMargin"],
            staticMovementConfig["movementThreshold"],
            staticMovementConfig["movementTimeout"],
            showFrame=debug,
        )

    def detect(self) -> bool:
        isEyelidActive = self.eyelidDetector.frameDetection()
        isImageStatic = self.staticMovementDetector.detectStatic()

        print(
            "isEyelidActive: {} \tisImageStatic: {}".format(
                isEyelidActive, isImageStatic
            )
        )

