import socket
import logging
import time

from raspi.gps.GPSHelper import GPSHelper
from raspi.gps.GPSObject import GPSObject
from raspi.utils.SerialHelper import SerialHelper

def main():
    print("Starting GPS Process")

    serial = SerialHelper("/dev/ttyS0")

    while True:
        serial.sendLine("at")
        try:
            serial.waitMessage("OK", 2000)
            print("Baud rate sync-ed")
            break;

        except:
            print("Retrying on baud rate correction...")

    gpsHelper = GPSHelper(serial)

    host = "127.0.0.1"
    port = 8080

    sensorSocket = socket.socket()
    sensorSocket.connect((host, port))

    while True:
        gpsInfo = gpsHelper.getGPSLocation()
        if gpsInfo.speed > 10:
            message = "GPS:TRUE\n\r"
        else:
            message = "GPS:FALSE\n\r"
        sensorSocket.send(message.encode())
        time.sleep(1)


if __name__ == "__main__":
    main()