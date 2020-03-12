import socket
import logging
import time
import json

from raspi.gps.GPSHelper import GPSHelper
from raspi.gps.GPSObject import GPSObject
from raspi.utils.SerialHelper import SerialHelper


def main():
    print("Starting GPS Process")

    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    gpsConfig = config["detectionConfig"]["gpsDetectionConfig"]

    serial = SerialHelper(gpsConfig["generalConfig"]["serialPort"])

    while True:
        serial.sendLine("at")
        try:
            serial.waitMessage("OK", 2000)
            print("Baud rate sync-ed")
            break

        except:
            print("Retrying on baud rate correction...")

    gpsHelper = GPSHelper(serial)

    host = "127.0.0.1"
    port = 8080

    sensorSocket = socket.socket()
    sensorSocket.connect((host, port))

    speedStopTime = int(time.time() * 1000)

    while True:

        # FOR DEBUG PURPOSE ONLY #

        sensorSocket.send("GPS:TRUE;10N,10E;".encode())
        time.sleep(1)
        continue

        # END OF DEBUG BLOCK #

        gpsInfo = gpsHelper.getGPSLocation()
        locationString = "{}{},{}{}".format(gpsInfo.latitude, gpsInfo.latitudeDirection, gpsInfo.longitude, gpsInfo.longitudeDirection)
        if gpsInfo.speed < gpsConfig["speedDetectionConfig"]["movingSpeedThreshold"]:
            if (int(time.time() * 1000) - speedStopTime) > gpsConfig[
                "speedDetectionConfig"
            ]["movingTimeThreshold"]:
                message = "GPS:TRUE;{};\n\r".format(locationString)
            else:
                message = "GPS:FALSE;{};\n\r".format(locationString)
        else:
            speedStopTime = int(time.time() * 1000)
            message = "GPS:FALSE;{};\n\r".format(locationString)
        sensorSocket.send(message.encode())
        time.sleep(1)


if __name__ == "__main__":
    main()
