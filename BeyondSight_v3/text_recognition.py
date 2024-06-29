import cv2 as cv
import pytesseract
from time import sleep
import os
from tts import speak

class TextRecognizer:
    def __init__(self, size=(640, 480)):
        self.size = size
        self.text_roi = (0, 0, size[0], size[1])
        self.keywords = {
            "fire", "enter", "exit", "department", "laboratory", "emergency", "assembly", "lab",
            "dept.", "university", "engineering", "ned", "telecommunications", "telecom", "telecommunication"
        }

    def recognize_text(self, img):
        img_resized = cv.resize(img, self.size)
        config = ('-l eng --oem 3 --psm 11')
        text = pytesseract.image_to_string(img_resized, config=config)
        detected_keywords = {keyword for keyword in self.keywords if keyword in text.lower()}

        if detected_keywords:
            for keyword in detected_keywords:
                print('Detected text: ', keyword)
                speak(f"Detected text: {keyword}")
        
        text_boxes = pytesseract.image_to_boxes(img_resized, config=config)
        locations_to_speak = []

        for box in text_boxes.splitlines():
            box = box.split(' ')
            x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            cv.rectangle(img_resized, (x, self.size[1] - y), (w, self.size[1] - h), (0, 255, 0), 2)
            text = ''.join(box[0])
            if any(keyword.lower() in text.lower() for keyword in self.keywords):
                center_x = (x + w) // 2
                if center_x < self.size[0] // 3:
                    location = 'left'
                elif center_x > self.size[0] * 2 // 3:
                    location = 'right'
                else:
                    location = 'center'
                locations_to_speak.append(f"{text} located at {location}")
        
        if locations_to_speak:
            for loc in locations_to_speak:
                speak(loc)

    def recognize_saved_picture(self, image):
        text = pytesseract.image_to_string(image)
        if text:
            print('Detected text: ', text)
            speak(f"Detected text: {text}")
        else:
            speak('No text detected')

# Example usage:
# recognizer = TextRecognizer()
# frame = cv.imread('image.jpg')  # Example image path
# recognizer.recognize_text(frame)


