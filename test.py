from raspi.detection.camera.EyelidDetectorTwo import EyelidDetector
from raspi.detection.camera.StaticMovementDetector import StaticMovementDetector
from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType
from raspi.detection.AccidentDetector import ImageBasedDetector, SensorBasedDetector
import sys
import json
import logging
import time
import cv2
import dlib
import re
from raspi.utils.datapresentation.GraphPlotter import GraphPlotter
from raspi.gps.GPSHelper import GPSHelper
from raspi.gps.GPSObject import GPSObject
from raspi.utils.SerialHelper import SerialHelper
from raspi.utils.TCPHelper import TCPHelper

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



########################
# Test for GPS Reading #
########################

# def main():
#     print("GPS Test")

#     serial = SerialHelper("/dev/ttyS0")
#     # logging.basicConfig(level=logging.DEBUG, filename="gpsPath.log")

#     while True:
#         serial.sendLine("at")
#         try:
#             serial.waitMessage("OK", 1000)
#             print("Baud rate sync-ed")
#             break;

#         except:
#             print("Retrying on baud rate correction...")

#     print("Setting up GPS Helper...")
#     gpsHelper = GPSHelper(serial)
#     print("Getting GPS location...")
#     while True:
#         gpsData = gpsHelper.getGPSLocation()

#         message = "Speed: {}".format(gpsData.speed)

#         print(message)
#         # logging.debug(message)


# if __name__ == "__main__":
#     main()


##############################
# Test for TCP/IP Connection #
##############################

# def main():
#     serial = SerialHelper("/dev/ttyS0")

#     while True:
#         serial.sendLine("at")
#         try:
#             serial.waitMessage("OK", 2000)
#             print("Baud rate sync-ed")
#             break;

#         except:
#             print("Retrying on baud rate correction...")


#     tcpHelper = TCPHelper(serial, "35.234.201.162", 8200, "celcom2g")
#     tcpHelper.initializeDevice()
#     tcpHelper.sendMessage("May the force be with you")
#     tcpHelper.sendMessage("So this is something")
#     tcpHelper.sendMessage("It's actually working")
#     tcpHelper.sendMessage("So cheers")
#     tcpHelper.sendMessage("Still can't believe it's actually working")
#     tcpHelper.sendMessage("But somehow, it works")

#     while True:
#         message = tcpHelper.readMessage()
#         print(message)
#         time.sleep(0.1)


# if __name__ == "__main__":
#     main() 


####################################
# Test for overall Image Detection #
####################################


def main():
    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    imageBasedDetector = ImageBasedDetector(
        CameraType.WEB_CAM,
        config["detectionConfig"]["imageDetectionConfig"],
        cameraConfig=config["generalConfig"]["camera"],
        debug=True,
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


###############
# Sensor Test #
###############

# def main():

#     print("Sensor Recording")
#     logging.basicConfig(level=logging.DEBUG, filename="sensorData.log")
    
#     with open("config.json") as jsonFile:
#         config = json.load(jsonFile)

#         sensorDetector = SensorBasedDetector(
#             config["detectionConfig"]["sensorDetectionConfig"]
#         )

#         initialTime = int(time.time() * 1000)

#         while True:
#             currentTime = int(time.time() * 1000)
#             timeLapsed = currentTime - initialTime

#             logString = sensorDetector.readValue()
#             logging.debug(logString)
#             time.sleep(0.05)


# if __name__ == "__main__":
#     main()


#############################################
# Test for Sensor Based Detection Recording #
#############################################


# def main():
#     print("Process Start")
#     logging.basicConfig(level=logging.DEBUG, filename="sensorData.log")
#     imageWindow = dlib.image_window()

#     with open("config.json") as jasonFile:
#         config = json.load(jasonFile)

#     sensorDetector = SensorBasedDetector(
#         config["detectionConfig"]["sensorDetectionConfig"]
#     )

#     camera = Camera(CameraType.WEB_CAM, config["generalConfig"]["camera"])

#     initialTime = 0

#     while True:

#         currentTime = int(time.time() * 1000)
#         if initialTime == 0:
#             initialTime = currentTime

#         timeLapsed = currentTime - initialTime

#         logString = sensorDetector.readValue()

#         frame = camera.takeFrame()
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         cv2.putText(frame, str(timeLapsed), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

#         imageWindow.set_image(frame)

#         cv2.imwrite("outImg/{}.jpg".format(timeLapsed), frame)

#         # logging.debug(logString)
#         print(logString)
#         time.sleep(0.05)
        



# if __name__ == "__main__":
#     main()



###########################
# Another logging attempt #
###########################

# def main():
#     print("Process Start")
#     logging.basicConfig(level=logging.DEBUG, filename="sensorData.log")

#     with open("config.json") as jsonFile:
#         config = json.load(jsonFile)

#     sensorDetector = SensorBasedDetector(config["detectionConfig"]["sensorDetectionConfig"])

#     initPattern = r"//\d+//"
#     initTime = 0

#     while True:
#         data = sensorDetector.readValue()
#         foundPattern = re.findall(initPattern, data)
#         if len(foundPattern) == 1:
#             initTime = int(foundPattern[0].replace("//", ""))
#             break
#         else:
#             print(data)

#     print("Break out")


# if __name__ == "__main__":
#     main()