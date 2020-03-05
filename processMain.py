from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from enum import Enum

class ProcessState(Enum):
    DETECT_INIT = 0,
    DETECT_START = 1,
    SENSOR_TRIGGER = 2,
    GPS_TRIGGER = 3,
    CAMERA_TRIGGER = 4,
    ACCIDENT_REPORT = 5


class TCPServer(Protocol):

    def __init__(self, currentState, sensorInitStatus):
        self.currentState = currentState
        self.sensorInitStatus = sensorInitStatus

    def dataReceived(self, data: bytes):
        receivedData = data.decode()

        if self.currentState == ProcessState.DETECT_INIT:
            print("State: Detection init")
            if "SENSOR" in receivedData:
                self.sensorInitStatus[0] = 1
            elif "CAMERA" in receivedData:
                self.sensorInitStatus[1] = 1

            print(self.sensorInitStatus)

            if self.sensorInitStatus[0] == 1 and self.sensorInitStatus[1] == 1:
                self.currentState = ProcessState.DETECT_START

        elif self.currentState == ProcessState.DETECT_START:
            print("State: Detection start")
            if "SENSOR" in receivedData and "TRUE" in receivedData:
                self.currentState = ProcessState.SENSOR_TRIGGER
                
        elif self.currentState == ProcessState.SENSOR_TRIGGER:
            print("State: Sensor triggered")
        elif self.currentState == ProcessState.GPS_TRIGGER:
            print("State: GPS Triggered")
        elif self.currentState == ProcessState.CAMERA_TRIGGER:
            print("State: Camera Triggered")
        elif self.currentState == ProcessState.ACCIDENT_REPORT:
            print("State: Accident Reporting")
        else:
            print("Invalid State")

class TCPServerFactory(Factory):

    def __init__(self):
        self.state = ProcessState.DETECT_INIT
        self.sensorInitStatus = [0, 0]

    def buildProtocol(self, addr):
        return TCPServer(self.state, self.sensorInitStatus)

endpoint = TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(TCPServerFactory())
reactor.run()