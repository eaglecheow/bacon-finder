import numpy


class DataObserver:
    def __init__(self, dataSize: int = 5, startingValue: float = 0):
        super().__init__()

        self.numberCount = 0
        self.rawData = [startingValue] * dataSize

    def calculateStd(self):
        self.stdValue = numpy.std(self.rawData, ddof=1)

    def calculateVar(self):
        self.varValue = numpy.var(self.rawData, ddof=1)

    def calculateMean(self):
        self.meanValue = numpy.mean(self.rawData)

    def calculateMedian(self):
        self.medianValue = numpy.median(self.rawData)

    def inputValue(self, value: float):
        self.numberCount += 1

        self.rawData.pop()
        self.rawData.insert(0, value)

        if self.numberCount < len(self.rawData):
            self.stdValue = 0
            self.varValue = 0
            self.meanValue = 0
            self.medianValue = 0

            return

        self.calculateStd()
        self.calculateVar()
        self.calculateMean()
        self.calculateMedian()
