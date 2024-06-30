import time
import libcamera
from picamera2 import Picamera2
import cv2 as cv

class Camera:
    def __init__(self, size=(320, 240)):
        self.picam = Picamera2()
        self.size = size
        config = self.picam.create_preview_configuration(main={"size": self.size})
        config["transform"] = libcamera.Transform(vflip=0)  # Vertical flip
        self.picam.configure(config)
        self.picam.start()
        
    def get_frame(self):
        img = self.picam.capture_array()
        ret = img is not None
        return ret, img

    def save_picture(self, img):
        img_resized = cv.resize(img, self.size)
        cv.imwrite('picture.jpg', img_resized)
        time.sleep(1)

    def cleanup(self):
        self.picam.stop()
        self.picam.close()
