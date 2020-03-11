import serial
import pynmea2
import time
from ..utils.SerialHelper import SerialHelper
import math
from .GPSObject import GPSObject


class GPSHelper:
    def __init__(self, serialObj: SerialHelper):
        super().__init__()

        self.serialObj = serialObj
        self.isOpen = False

        messagePair = [["AT+CGNSPWR=1", "OK"]]

        self.serialObj.communicate(messagePair)


    def getGPSLocation(self, timeout=10000):

        startTime = time.time() * 1000

        while True:
            time.sleep(1)
            self.serialObj.sendLine("AT+CGNSINF")

            while True:
                responseString = self.serialObj.readLine()
                if "+CGNSINF:" in responseString:
                    break

            responseString = responseString.replace("+CGNSINF:", "")

            responseData = responseString.split(",")

            # Invalid GPS
            if responseData[2] == "":
                continue

            gpsObject = GPSObject()

            if responseData[2] != "":
                responseData[2] = responseData[2][0:-5]
            gpsObject.timeStamp = int(responseData[2])
            gpsObject.latitude = abs(float(responseData[3]))
            if float(responseData[3]) >= 0:
                gpsObject.latitudeDirection = "N"
            else:
                gpsObject.latitudeDirection = "S"
            gpsObject.longitude = abs(float(responseData[4]))
            if float(responseData[4]) >= 0:
                gpsObject.longitudeDirection = "E"
            else:
                gpsObject.longitudeDirection = "W"
            gpsObject.altitude = float(responseData[5])
            gpsObject.altitudeUnits = "M"
            gpsObject.speed = float(responseData[6])
            if responseData[14] == "":
                responseData[14] = "0"
            if responseData[15] == "":
                responseData[15] = "0"
            if responseData[16] == "":
                responseData[16] = "0"

            gpsObject.satelliteAmount = int(responseData[14]) + int(responseData[15]) + int(responseData[16])

            if gpsObject.checkDataValidity() == True:
                return gpsObject
            elif ((time.time() * 1000) - startTime) > timeout:
                raise Exception("[GPS] Timeout while getting GPS location")
            else:
                continue


