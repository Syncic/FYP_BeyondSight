import cv2 as cv

class Camera:
    def __init__(self, size=(320, 240)):
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, size[0])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, size[1])

    def get_frame(self):
        ret, img = self.cap.read()
        return ret, img

    def save_picture(self, img):
        cv.imwrite('picture.jpg', img)

    def cleanup(self):
        self.cap.release()

