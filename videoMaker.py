import cv2
import numpy as np
import os
from os.path import isfile, join

imageDirectory = "outImg/"

frameArray = []
fileArray = [frame for frame in os.listdir(imageDirectory) if isfile(join(imageDirectory, frame))]

fileArray.sort(key = lambda x: int(x[0:-4]))

for i in range(len(fileArray)):
    filename = imageDirectory + fileArray[i]
    img = cv2.imread(filename)

    if img.shape == None:
        continue

    height, width, layers = img.shape
    size = (width, height)
    print(filename)
    frameArray.append(img)

outputVideo = cv2.VideoWriter("outVid.avi", cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

for i in range(len(frameArray)):
    outputVideo.write(frameArray[i])

outputVideo.release()