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

    @staticmethod
    def parseGps(dataString: str) -> GPSObject:
        msg = pynmea2.parse(dataString)

        if msg.lat == "":
            lat = 0
        else:
            lat: float = float(msg.lat)

        if msg.lon == "":
            lon = 0
        else:
            lon: float = float(msg.lon)

        latDegree = math.floor(lat / 100)
        latMinute = ((lat / 100) - latDegree) * 100

        lonDegree = math.floor(lon / 100)
        lonMinute = ((lon / 100) - lonDegree) * 100

        gpsObject = GPSObject()
        gpsObject.timeStamp = msg.timestamp
        gpsObject.latitude = latDegree + (latMinute / 60)
        gpsObject.latitudeDirection = msg.lat_dir
        gpsObject.longitude = lonDegree + (lonMinute / 60)
        gpsObject.longitudeDirection = msg.lon_dir
        gpsObject.altitude = msg.altitude
        gpsObject.altitudeUnits = msg.altitude_units
        gpsObject.satelliteAmount = msg.num_sats

        return gpsObject

    def getGPSLocation(self, timeout=10000):

        startTime = time.time() * 1000

        if self.isOpen == True:
            return

        try:
            self.serialObj.waitPattern("GGA", 2000)
        except Exception:
            messagePair = [["AT+CGNSPWR=1", "OK"], ["AT+CGNSTST=1", "OK"]]

            self.serialObj.communicate(messagePair)

        while True:

            response = self.serialObj.readLine()

            if not response.find("GGA") > 0:
                continue

            gpsObject = self.parseGps(response)

            if gpsObject.checkDataValidity() == True:
                return gpsObject

            currentTime = time.time() * 1000
            if (currentTime - startTime) > timeout:
                raise Exception("[GPS] Timeout while getting GPS location")

