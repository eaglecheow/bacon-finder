import cv2
import numpy as np
import os
from os.path import isfile, join
import sys

if sys.argv[1]:
    imageDirectory = sys.argv[1]
else:
    imageDirectory = "outImg/"

frameArray = []
fileArray = [frame for frame in os.listdir(imageDirectory) if isfile(join(imageDirectory, frame))]

fileArray.sort(key = lambda x: int(x[0:-4]))

for i in range(len(fileArray)):
    filename = imageDirectory + fileArray[i]
    img = cv2.imread(filename)

    try:
        height, width, layers = img.shape
    except:
        continue
    size = (width, height)
    print(filename)
    frameArray.append(img)

outputVideo = cv2.VideoWriter("outVid.avi", cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

for i in range(len(frameArray)):
    outputVideo.write(frameArray[i])

outputVideo.release()