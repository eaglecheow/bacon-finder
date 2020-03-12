import socket
import logging
import time
import json

from raspi.detection.AccidentDetector import SensorBasedDetector


def main():
    print("Starting Sensor Process")

    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    sensorDetector = SensorBasedDetector(
        config["detectionConfig"]["sensorDetectionConfig"]
    )

    host = "127.0.0.1"
    port = 8080

    sensorSocket = socket.socket()
    sensorSocket.connect((host, port))

    while True:

        # FOR DEBUG PURPOSE ONLY #

        sensorSocket.send("SENSOR:TRUE".encode())
        time.sleep(1)
        continue

        # END OF DEBUG BLOCK #

        sensorResult = sensorDetector.detect()
        if sensorResult == True:
            message = "SENSOR:TRUE\n\r"
        else:
            message = "SENSOR:FALSE\n\r"
        sensorSocket.send(message.encode())
        time.sleep(1)


if __name__ == "__main__":
    main()
