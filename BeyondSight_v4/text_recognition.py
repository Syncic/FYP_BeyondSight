import cv2 as cv
import pytesseract
from tts import speak


class TextRecognizer:
    def __init__(self, size=(640, 480)):
        self.size = size
        self.keywords = {
            "fire", "enter", "exit", "department", "laboratory", "emergency", "assembly", "lab",
            "dept.", "university", "engineering", "ned", "telecommunications", "telecom", "telecommunication"
        }
        
    def recognize_text(self, img):
        if img.shape[0] > self.size[1] or img.shape[1] > self.size[0]:
            img_resized = cv.resize(img, self.size)
        else:
            img_resized = img

        config = '-l eng --oem 3 --psm 11'
        text = pytesseract.image_to_string(img_resized, config=config).lower()

        detected_keywords = [keyword for keyword in self.keywords if keyword in text]

        if detected_keywords:
            messages = [f"Detected text: {keyword}" for keyword in detected_keywords]
            speak(". ".join(messages))

        text_boxes = pytesseract.image_to_boxes(img_resized, config=config).splitlines()
        locations_to_speak = []

        for box in text_boxes:
            box = box.split(' ')
            x, y, w, h = map(int, box[1:5])
            detected_text = box[0]
            if any(keyword in detected_text.lower() for keyword in self.keywords):
                center_x = (x + w) // 2
                if center_x < self.size[0] // 3:
                    location = 'left'
                elif center_x > self.size[0] * 2 // 3:
                    location = 'right'
                else:
                    location = 'center'
                locations_to_speak.append(f"{detected_text} located at {location}")
                cv.rectangle(img_resized, (x, self.size[1] - y), (w, self.size[1] - h), (0, 255, 0), 2)

        if locations_to_speak:
            speak(". ".join(locations_to_speak))

    def recognize_saved_picture(self, image):
        text = pytesseract.image_to_string(image).lower()
        detected_keywords = [keyword for keyword in self.keywords if keyword in text]

        if detected_keywords:
            messages = [f"Detected text: {keyword}" for keyword in detected_keywords]
            speak(". ".join(messages))
        else:
            speak('No text detected')

# Example usage:
# recognizer = TextRecognizer()
# frame = cv.imread('image.jpg')  # Example image path
# recognizer.recognize_text(frame)
