import cv2 as cv
import time
import pytesseract

from BeyondSightTextToSpeech import speak 


tessaractAddress = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pytesseract.pytesseract.tesseract_cmd = tessaractAddress


def pic_to_text(frame, new_detections):
    cv.imwrite('picture right eye.jpg', frame)
    time.sleep(1)
    image = cv.imread('picture right eye.jpg')
    text = pytesseract.image_to_string(image)
    if text == '' or text == new_detections:
        print('No text detected')
        speak('text not found')
    else:
        print('Detected text: ', text)
        speak(f'Detected text: {text}')
