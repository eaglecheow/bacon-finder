import sys
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np



inputFile = sys.argv[1]

pattern = r"X:\d+;Y:\d+;Z:\d+;"

fileContent = open(inputFile, "r")

dataListX = []
dataListY = []
dataListZ = []

for line in fileContent:
    foundPattern = re.findall(pattern, line)
    for content in foundPattern:
        xPattern = r"X:\d+;"
        yPattern = r"Y:\d+;"
        zPattern = r"Z:\d+;"

        foundX: str = re.findall(xPattern, content)[0]
        foundY = re.findall(yPattern, content)[0]
        foundZ = re.findall(zPattern, content)[0]

        x = int(foundX.replace("X:", "").replace(";", ""))
        y = int(foundY.replace("Y:", "").replace(";", ""))
        z = int(foundZ.replace("Z:", "").replace(";", ""))

        dataListX.append(x)
        dataListY.append(y)
        dataListZ.append(z)

t = np.arange(0, len(dataListX), 1)

fig, ax = plt.subplots()
ax.plot(t, dataListX, label='x')
ax.plot(t, dataListY, label='y')
ax.plot(t, dataListZ, label='z')
ax.set(xlabel='time', ylabel='data')
ax.grid()
ax.legend()

plt.show()

