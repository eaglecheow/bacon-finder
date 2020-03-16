import socket
import logging
import time
import json

from raspi.gps.GPSHelper import GPSHelper
from raspi.gps.GPSObject import GPSObject
from raspi.utils.SerialHelper import SerialHelper
from raspi.utils.TCPHelper import TCPHelper


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
    tcpHelper = TCPHelper(serial, "35.234.201.162", 8200, "celcom2g")
    tcpHelper.initializeDevice()


    host = "127.0.0.1"
    port = 8080

    sensorSocket = socket.socket()
    sensorSocket.connect((host, port))

    speedStopTime = int(time.time() * 1000)

    previousData = ["0,0,0"] * 20 # Latitude,Longitude,Speed

    while True:

        # FOR DEBUG PURPOSE ONLY #

        sensorSocket.send("GPS:TRUE;10N,10E;".encode())
        time.sleep(1)
        
        recvData = sensorSocket.recv(1024).decode()
        if "AD ->" in recvData:
            tcpHelper.sendMessage(recvData)

        continue

        # END OF DEBUG BLOCK #

        gpsInfo = gpsHelper.getGPSLocation()
        # locationString = "{}{},{}{}".format(gpsInfo.latitude, gpsInfo.latitudeDirection, gpsInfo.longitude, gpsInfo.longitudeDirection)

        previousData = previousData[1:20] + ["{},{},{}".format(gpsInfo.latitude, gpsInfo.longitude, gpsInfo.speed)]

        locationString = ""
        for locationData in previousData:
            locationString += "{};".format(locationData)

        if gpsInfo.speed < gpsConfig["speedDetectionConfig"]["movingSpeedThreshold"]:
            if (int(time.time() * 1000) - speedStopTime) > gpsConfig[
                "speedDetectionConfig"
            ]["movingTimeThreshold"]:
                message = "GPS:TRUE;{}\n\r".format(locationString)
            else:
                message = "GPS:FALSE;{}\n\r".format(locationString)
        else:
            speedStopTime = int(time.time() * 1000)
            message = "GPS:FALSE;{}\n\r".format(locationString)
        sensorSocket.send(message.encode())

        recvData = sensorSocket.recv(1024).decode()
        if "AD ->" in recvData:
            tcpHelper.sendMessage(recvData)
            
        time.sleep(1)


if __name__ == "__main__":
    main()
