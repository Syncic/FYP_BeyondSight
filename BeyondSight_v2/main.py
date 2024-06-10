import cv2 as cv
from time import sleep
from tts import speak
import tts
from camera import Camera
from audio import AudioHandler
from object_detection import ObjectDetector
from text_recognition import TextRecognizer


# Initialize modules
camera = Camera()
audio_handler = AudioHandler()
object_detector = ObjectDetector()
text_recognizer = TextRecognizer()

speak("Hello! I am Tecto, your Navigational Aid", tts.SLOW_VOICE_RATE)
sleep(1)
speak("System: Booting UP!", tts.SLOW_VOICE_RATE)

frame_count = 0

while True:
    ret, img = camera.get_frame()
    if not ret:
        speak("video input failed... Exiting...", tts.SLOW_VOICE_RATE)
        break

    frame_count += 1
    frame_divident = 5 # should be greater than 4

    if frame_count % frame_divident == 0:
        object_detector.detect_objects(img)
        text_recognizer.recognize_text(img)

    key = cv.waitKey(1)
    
    if key == ord('p'):
        speak("reading frame for text")
        text_recognizer.recognize_saved_picture(image=img)

    if key == ord('z'):
        audio_handler.start_recording()
        while audio_handler.recording:
            key = cv.waitKey(1) & 0xFF
            if key == ord('z'):
                audio_handler.stop_recording()
                break
            
            try:
                data = audio_handler.stream.read(audio_handler.chunk)
                audio_handler.frames.append(data)
            except KeyboardInterrupt:
                print("Keyboard interrupt received. Stopping recording.")
                speak("interrupted...")
                audio_handler.recording = False
                break

    if key == ord('q'):
        speak("shutting down...")
        break

camera.cleanup()
audio_handler.cleanup()
cv.destroyAllWindows()
