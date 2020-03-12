import socket
import logging
import time
import json

from raspi.detection.AccidentDetector import ImageBasedDetector
from raspi.utils.camera.CameraType import CameraType


def main():
    print("Starting Camera Process")

    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    imageDetector = ImageBasedDetector(
        CameraType.WEB_CAM,
        config["detectionConfig"]["imageDetectionConfig"],
        config["generalConfig"]["camera"],
    )

    host = "127.0.0.1"
    port = 8080

    sensorSocket = socket.socket()
    sensorSocket.connect((host, port))

    while True:

        # FOR DEBUG PURPOSE ONLY #
        # imageDetector = None
        # sensorSocket.send("CAMERA:TRUE".encode())
        # time.sleep(1)
        # continue

        # END OF DEBUG BLOCK #

        imageResult = imageDetector.detect()
        if imageResult == True:
            message = "CAMERA:TRUE\n\r"
        else:
            message = "CAMERA:FALSE\n\r"
        sensorSocket.send(message.encode())
        time.sleep(0.1)


if __name__ == "__main__":
    main()
