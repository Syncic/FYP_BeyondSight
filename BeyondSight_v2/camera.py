import cv2 as cv
from time import sleep

class Camera:
    def __init__(self, size=(320, 240), fps=30):
        self.cap = cv.VideoCapture(0)
        self.size = size
        self.fps = fps
        self.n = 0

    def get_frame(self):
        ret, img = self.cap.read()
        return ret, img

    def save_picture(self, img):
        img_resized = cv.resize(img, self.size)
        cv.imwrite('picture.jpg', img_resized)
        sleep(1)

    def cleanup(self):
        self.cap.release()
