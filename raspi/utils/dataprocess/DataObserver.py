import numpy


class DataObserver:
    def __init__(self, dataSize: int = 5, startingValue: float = 0):
        super().__init__()

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
        self.rawData.pop()
        self.rawData.insert(0, value)

        self.calculateStd()
        self.calculateVar()
        self.calculateMean()
        self.calculateMedian()
