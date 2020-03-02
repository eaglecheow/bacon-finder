from raspi.detection.AccidentDetector import SensorBasedDetector

import time
import logging
import json

def main():
    print("Process Start")
    logging.basicConfig(level=logging.DEBUG, filename="sensorData.log")

    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    sensorDetector = SensorBasedDetector(config["detectionConfig"]["sensorDetectionConfig"])

    while True:
        currentTime = int(time.time() * 1000)

        sensorValues = sensorDetector.readValue()

        logString = "[{}]{}".format(currentTime, sensorValues)

        logging.debug(logString)


if __name__ == "__main__":
    main()
