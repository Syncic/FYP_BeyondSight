import cv2 as cv
from time import sleep
from tts import speak
import tts
from camera import Camera
from audio import AudioHandler
from object_detection import ObjectDetector
from text_recognition import TextRecognizer
from Simple_facerec import SimpleFacerec

# Initialize modules
camera = Camera()
audio_handler = AudioHandler()
object_detector = ObjectDetector()
text_recognizer = TextRecognizer()
face_recognizer = SimpleFacerec()

# Load face encodings
face_recognizer.load_encoding_images("C:/random_path_to_img")

'''speak("Hello! I am Tecto, your Navigational Aid", tts.SLOW_VOICE_RATE)
sleep(1)
speak("System: Booting UP!", tts.SLOW_VOICE_RATE)'''

frame_count = 0
frame_divident = 5  # should be greater than 4
previous_name = "Unknown"

while True:
    ret, img = camera.get_frame()
    if not ret:
        speak("video input failed... Exiting...", tts.SLOW_VOICE_RATE)
        break

    frame_count += 1

    # Face recognition
    face_locations, face_names = face_recognizer.detect_known_faces(img)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        
        # Remove numbers from the name
        clean_name = ''.join(filter(str.isalpha, name))
        
        cv.putText(img, clean_name, (x1, y1 - 10), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 200), 3)
        
        if clean_name!= "Unknown" and clean_name!= previous_name:
            speak(f"{clean_name}", tts.SLOW_VOICE_RATE)
            previous_name = clean_name
        elif clean_name == "Unknown" and previous_name!= "Unknown":
            previous_name = "Unknown"

    
    # Object detection and text recognition every frame_divident frames
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
