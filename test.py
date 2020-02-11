from raspi.detection.camera.EyelidDetector import EyelidDetector
from raspi.detection.camera.StaticMovementDetector import StaticMovementDetector
from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType
from raspi.detection.AccidentDetector import ImageBasedDetector
import sys
import json

############################
# Test for Eyelid Detector #
############################

# predictionFilePath = sys.argv[1]

# camera = Camera(CameraType.WEB_CAM)
# eyelidDetector = EyelidDetector(
#     predictionFilePath, camera, eyelidMovementTimeout=5000, showFrame=True
# )

# while True:
#     print("IsActive: {}".format(eyelidDetector.frameDetection()))


##################################
# Test for Static Video Detector #
##################################

# camera = Camera(CameraType.WEB_CAM)
# staticDetector = StaticMovementDetector(camera, 50, 3, 5000, True)

# while True:
#     print("IsStatic: {}".format(staticDetector.detectStatic()))


####################################
# Test for overall Image Detection #
####################################


def main():
    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    imageBasedDetector = ImageBasedDetector(
        CameraType.WEB_CAM,
        config["detectionConfig"]["imageDetectionConfig"],
        debug=False,
    )

    while True:
        imageBasedDetector.detect()


if __name__ == "__main__":
    main()


##############################
# Test load JSON config file #
##############################

# with open('config.json') as jsonFile:
#     data = json.load(jsonFile)

# print(data["detectionConfig"]["imageDetectionConfig"]["eyelidDetectionConfig"]["faceModelFilePath"])
