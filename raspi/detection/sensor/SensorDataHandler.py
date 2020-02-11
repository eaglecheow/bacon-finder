from raspi.utils.SerialHelper import SerialHelper


class SensorDataHandler:
    def __init__(self, config):
        super().__init__()

        generalConfig = config["generalConfig"]

        self.serialObject = SerialHelper(
            generalConfig["arduinoSerialPort"], generalConfig["arduinoBaudRate"]
        )


    def readValue(self):

        sensorData = self.serialObject.readLine()
        

