# main.py

import cv2 as cv
from time import sleep
from tts import speak
from camera import Camera
from audio_2 import AudioHandler
from object_detection import ObjectDetector
from text_recognition import TextRecognizer

# Initialize modules
camera = Camera()
audio_handler = AudioHandler()
object_detector = ObjectDetector()
text_recognizer = TextRecognizer()

speak("Hello! I am Tecto, your Navigational Aid")
sleep(1)
speak("System: Booting UP!")

frame_count = 0

while True:
    ret, img = camera.get_frame()
    if not ret:
        speak("video input failed... Exiting...")
        break

    frame_count += 1
    frame_divident = 5  # should be greater than 4

    if frame_count % frame_divident == 0:
        object_detector.detect_objects(img)
        text_recognizer.recognize_text(img)

    key = cv.waitKey(1)

    if key == ord('p'):
        # camera.save_picture(img)
        speak("reading frame for text")
        text_recognizer.recognize_saved_picture(image=img)

    if key == ord('z'):
        if not audio_handler.recording:
            audio_handler.start_recording()
        else:
            audio_handler.stop_recording()
            speak("processing...")

    if key == ord('q'):
        speak("shutting down...")
        break

camera.cleanup()
audio_handler.cleanup()
cv.destroyAllWindows()
