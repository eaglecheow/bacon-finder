import os
import re

class SensorLogParser:


    @staticmethod
    def parseFile(logFilePath):
        if not os.path.isfile(logFilePath):
            raise Exception("Invalid log file path")

        fileContent = open(logFilePath, "r")

        pattern = r"\[\d+\]X:\d+;Y:\d+;Z:\d+;V:\d+;"

        timeList = []
        dataListX = []
        dataListY = []
        dataListZ = []
        dataListV = []

        for line in fileContent:
            foundPattern = re.findall(pattern, line)
            for content in foundPattern:
                timePattern = r"\[\d+\]"
                xPattern = r"X:\d+;"
                yPattern = r"Y:\d+;"
                zPattern = r"Z:\d+;"
                vPattern = r"V:\d+;"

                foundTime = re.findall(timePattern, content)[0]
                foundX: str = re.findall(xPattern, content)[0]
                foundY = re.findall(yPattern, content)[0]
                foundZ = re.findall(zPattern, content)[0]
                foundV = re.findall(vPattern, content)[0]

                time = int(foundTime.replace("[", "").replace("]", ""))
                x = int(foundX.replace("X:", "").replace(";", ""))
                y = int(foundY.replace("Y:", "").replace(";", ""))
                z = int(foundZ.replace("Z:", "").replace(";", ""))
                v = int(foundV.replace("V:", "").replace(";", ""))

                timeList.append(time)
                dataListX.append(x)
                dataListY.append(y)
                dataListZ.append(z)
                dataListV.append(v)

        return (timeList, dataListX, dataListY, dataListZ, dataListV)