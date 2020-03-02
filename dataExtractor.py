import sys
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np



inputFile = sys.argv[1]

pattern = r"\[\d+\]X:\d+;Y:\d+;Z:\d+;V:\d+;"

fileContent = open(inputFile, "r")

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

# initialTime = timeList[0]

t = timeList

fig, ax = plt.subplots()
ax.plot(t, dataListX, label='x')
ax.plot(t, dataListY, label='y')
ax.plot(t, dataListZ, label='z')
ax.plot(t, dataListV, label='v')
ax.set(xlabel='time (ms)', ylabel='data')
ax.grid()
ax.legend()

plt.show()

