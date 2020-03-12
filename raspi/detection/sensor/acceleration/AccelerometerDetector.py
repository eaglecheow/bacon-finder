from raspi.utils.dataprocess.DataObserver import DataObserver

import math


class AccelerometerDetector:
    def __init__(self, accMeterConfig):
        super().__init__()

        self.resultantThreshold = accMeterConfig["resultantThreshold"]
        self.minTimingThreshold = accMeterConfig["minTimingThreshold"]
        self.maxTimingThreshold = accMeterConfig["maxTimingThreshold"]

        self.dataObserver = DataObserver()

        self.exceedThresholdStartTime = 0
        self.prevTime = int(time.time() * 1000)

    def detect(self, xAcc: int, yAcc: int, zAcc: int) -> bool:

        currentTime = int(time.time() * 1000)

        resultantAcc = math.sqrt((xAcc ** 2) + (yAcc ** 2) + (zAcc ** 2))

        self.dataObserver.inputValue(resultantAcc)

        if self.dataObserver.stdValue > self.resultantThreshold:
            self.exceedThresholdStartTime += currentTime - self.prevTime
        else:
            self.exceedThresholdStartTime = 0

        self.prevTime = currentTime

        if (
            self.exceedThresholdStartTime > self.minTimingThreshold
            and self.exceedThresholdStartTime < self.maxTimingThreshold
        ):
            return True
        else:
            return False

