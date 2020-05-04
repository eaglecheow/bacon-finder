import sys
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

from raspi.utils.dataprocess.DataObserver import DataObserver


inputFile = sys.argv[1]

do = DataObserver()

pattern = r"\[\d+\]X:\d+;Y:\d+;Z:\d+;"

fileContent = open(inputFile, "r")

timeList = []
dataListX = []
dataListY = []
dataListZ = []
# dataListV = []

for line in fileContent:
    foundPattern = re.findall(pattern, line)
    for content in foundPattern:
        timePattern = r"\[\d+\]"
        xPattern = r"X:\d+;"
        yPattern = r"Y:\d+;"
        zPattern = r"Z:\d+;"
        # vPattern = r"V:\d+;"

        foundTime = re.findall(timePattern, content)[0]
        foundX: str = re.findall(xPattern, content)[0]
        foundY = re.findall(yPattern, content)[0]
        foundZ = re.findall(zPattern, content)[0]
        # foundV = re.findall(vPattern, content)[0]

        time = int(foundTime.replace("[", "").replace("]", ""))
        x = int(foundX.replace("X:", "").replace(";", ""))
        y = int(foundY.replace("Y:", "").replace(";", ""))
        z = int(foundZ.replace("Z:", "").replace(";", ""))
        # v = int(foundV.replace("V:", "").replace(";", ""))

        timeList.append(time)
        dataListX.append(x)
        dataListY.append(y)
        dataListZ.append(z)
        # dataListV.append(v)

# initialTime = timeList[0]

sumList = []
sdList = []

for i in range(len(dataListX)):
    resultant = math.sqrt((dataListX[i] ** 2) + (dataListY[i] ** 2) + (dataListZ[i] ** 2))
    sumList.append(resultant)
    do.inputValue(resultant)
    sdList.append(do.stdValue)


t = timeList

fig, ax = plt.subplots()
ax.plot(t, dataListX, label='x')
ax.plot(t, dataListY, label='y')
ax.plot(t, dataListZ, label='z')
# ax.plot(t, dataListV, label='v')
# ax.plot(t, sumList, label='resultant')
# ax.plot(t, sdList, label='std')
ax.set(xlabel='time (ms)', ylabel='data')
# ax.axhline(20)
ax.grid()
ax.legend()

plt.show()

