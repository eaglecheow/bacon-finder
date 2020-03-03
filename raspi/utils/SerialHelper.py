import serial
from serial import SerialException
import time
import datetime
import logging
import re
from typing import List, Tuple

class SerialHelper:
    def __init__(self, port: str, baudRate: int = 9600, doNotOpen: bool = False):
        super().__init__()

        self.port = port
        self.baudRate = baudRate
        self.serialObject = serial.Serial(port, baudRate, xonxoff=0, rtscts=0, timeout=1, write_timeout=1)

        if doNotOpen == False:
            self.openSerial()

    def openSerial(self):

        if self.serialObject.is_open == False:
            self.serialObject.open()

    def sendCtrlZ(self):
        if self.serialObject.is_open == False:
            raise Exception("[Serial] Trying to send data with closed serial")

        self.serialObject.write("\x1A".encode() + b"\r\n")

    def sendLine(self, text: str):
        if self.serialObject.is_open == False:
            raise Exception("[Serial] Trying to send data with closed serial")

        textInByte = text.encode() + b"\r\n"
        self.serialObject.write(textInByte)

    def readLine(self) -> str:
        if self.serialObject.is_open == False:
            raise Exception("[Serial] Trying to read data with closed serial")

        returnMessage = self.serialObject.readline().decode().strip("\r\n")
        print("[{}] {}".format(datetime.datetime.now().time(), returnMessage))

        return returnMessage

    def waitMessage(
        self, matchingString: str, timeout: int = 10000, errorMessage: str = None
    ):
        startTime = time.time() * 1000

        while True:
            message = self.readLine()
            if message == matchingString:
                return

            currentTime = time.time() * 1000

            if (currentTime - startTime) > timeout:

                msg = errorMessage

                if msg == None:
                    msg = "[Serial] Timeout while waiting for expected message: {}".format(
                        matchingString
                    )

                raise Exception(msg)

    def waitPattern(
        self, matchingPattern: str, timeout: int = 10000, errorMessage: str = None
    ):

        startTime = time.time() * 1000

        while True:
            message = self.readLine()

            matches = re.findall(matchingPattern, message)
            if len(matches) == 1:
                return

            currentTime = time.time() * 1000

            if (currentTime - startTime) > timeout:

                msg = errorMessage

                if msg == None:
                    msg = "[Serial] Timeout while waiting for expected pattern: {}".format(
                        matchingPattern
                    )

                raise Exception(msg)

    def communicate(self, messagePairList: List[Tuple[str, str]]):

        for messagePair in messagePairList:

            messageToSend = messagePair[0]
            messageToExpect = messagePair[1]

            if not messageToSend.startswith("[EMPTY]"):
                try:
                    self.sendLine(messageToSend)
                except SerialException:
                    print("Disconnect detected while writing")

            readSuccess = False

            while readSuccess == False:

                try:
                    if messageToExpect.startswith("[REGEX]"):

                        messageToExpect = messageToExpect.replace("[REGEX]", "")

                        self.waitPattern(messageToExpect)
                    else:
                        self.waitMessage(messageToExpect)

                    readSuccess = True

                except SerialException:
                    print("Disconnect detected while reading")
                    print("Reopening serial...")
                    self.openSerial()