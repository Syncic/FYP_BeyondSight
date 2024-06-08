import cv2 as cv
import pytesseract
import os
from tts import speak

class TextRecognizer:
    def __init__(self, size=(320, 240)):
        self.size = size
        self.text_roi = (0, 0, size[0], size[1])
        self.keywords = ["fire", "enter", "exit", "department", "laboratory"]

    def recognize_text(self, img):
        img_resized = cv.resize(img, self.size)
        config = ('-l eng --oem 3 --psm 11')
        text_boxes = pytesseract.image_to_boxes(img_resized, config=config)
        for box in text_boxes.splitlines():
            box = box.split(' ')
            x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            cv.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = ''.join(box[5:])
            if any(keyword.lower() in text.lower() for keyword in self.keywords):
                print('Detected text: ', text)
                center_x = x + w // 2
                if center_x < self.size[0] // 3:
                    location = 'left'
                elif center_x > self.size[0] * 2 // 3:
                    location = 'right'
                else:
                    location = 'center'
                speak(f"{text} located at {location}")

    def recognize_saved_picture(self):
        image = cv.imread('picture.jpg')
        text = pytesseract.image_to_string(image)
        if text:
            print('Detected text: ', text)
            speak(f"Detected text: {text}")
        else:
            speak('No text detected')

        os.remove("picture.jpg")

