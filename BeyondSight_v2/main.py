import cv2 as cv
from tts import speak
from camera import Camera
from audio import AudioHandler
from object_detection import ObjectDetector
from text_recognition import TextRecognizer

# Initialize modules
camera = Camera()
audio_handler = AudioHandler()
object_detector = ObjectDetector()
text_recognizer = TextRecognizer()

speak("Hello! I am Beyond Sight: A real-time aid in navigation for the visually impaired")
speak("System: Booting UP!")

while True:
    ret, img = camera.get_frame()
    if not ret:
        speak("video input failed... Exiting...")
        break

    object_detector.detect_objects(img)
    text_recognizer.recognize_text(img)

    key = cv.waitKey(1)
    
    if key == ord('p'):
        camera.save_picture(img)
        speak("reading frame for text")
        text_recognizer.recognize_saved_picture()

    if key == ord('z'):
        speak("recording...")
        audio_handler.start_recording()
        while audio_handler.recording:
            key = cv.waitKey(1) & 0xFF
            if key == ord('z'):
                audio_handler.stop_recording()
                speak("processing...")
                break

    if key == ord('q'):
        speak("shutting down...")
        break

camera.cleanup()
audio_handler.cleanup()
cv.destroyAllWindows()
