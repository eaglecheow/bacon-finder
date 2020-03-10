from raspi.utils.camera.Camera import Camera
from raspi.utils.camera.CameraType import CameraType

import json
import cv2
import time
import dlib

def main():

    with open("config.json") as jsonFile:
        config = json.load(jsonFile)

    camera = Camera(CameraType.WEB_CAM, config["generalConfig"]["camera"])

    imageWindow = dlib.image_window()
    imageWindow.set_title("Image")

    while True:
        image = camera.takeFrame()

        currentTime = int(time.time() * 1000)

        cv2.putText(image, str(currentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

        imageWindow.set_image(image)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite("outImg/{}.jpg".format(currentTime), image)


if __name__ == "__main__":
    main()