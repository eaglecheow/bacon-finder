from raspi.detection.AccidentDetector import SensorBasedDetector
from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType

import logging
import json

def main():
    print("Process Start")
    logging.basicConfig(level=logging.DEBUG, filename="sensorData.log")

    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    sensorDetector = SensorBasedDetector(config["detectionConfig"]["sensorDetectionConfig"])

    while True:
        if sensorDetector.readValue == 0:
            break

        

    