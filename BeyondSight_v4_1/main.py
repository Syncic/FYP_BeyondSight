import cv2 as cv
from time import sleep
from tts import speak
import tts
from picamera import Camera
from audio import AudioHandler
from object_detection import ObjectDetector
from text_recognition import TextRecognizer
from Simple_facerec import SimpleFacerec

def main():
    # Initialize modules
    camera = Camera(size=(640, 480))  # Adjusted size for faster processing
    audio_handler = AudioHandler()
    object_detector = ObjectDetector()
    text_recognizer = TextRecognizer()
    face_recognizer = SimpleFacerec()

    # Load face encodings
    face_recognizer.load_encoding_images("C:/random_path_to_img")

    '''
    speak("Hello! I am Tecto, your Navigational Aid", tts.SLOW_VOICE_RATE)
    sleep(1)
    speak("System: Booting UP!", tts.SLOW_VOICE_RATE)
    '''

    frame_count = 0
    frame_divident = 8  # should be greater than 4
    previous_name = "Unknown"

    try:
        while True:
            ret, img = camera.get_frame()
            if not ret:
                speak("Video input failed... Exiting...", tts.SLOW_VOICE_RATE)
                break

            # Convert image from RGBA to RGB if it has 4 channels
            if img.shape[2] == 4:
                img = cv.cvtColor(img, cv.COLOR_RGBA2RGB)

            frame_count += 1

            # Face recognition every frame_divident frame
            if frame_count % frame_divident == 1:
                face_locations, face_names = face_recognizer.detect_known_faces(img)
                detected_names = set()
                for face_loc, name in zip(face_locations, face_names):
                    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                    # Remove numbers from the name
                    clean_name = ''.join(filter(str.isalpha, name))

                    cv.putText(img, clean_name, (x1, y1 - 10), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                    cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 200), 3)

                    if clean_name != "Unknown":
                        detected_names.add(clean_name)

                if detected_names and detected_names != {previous_name}:
                    for name in detected_names:
                        speak(f"{name}", tts.SLOW_VOICE_RATE)
                    previous_name = detected_names.pop()  # Update previous_name with the last detected name
                elif not detected_names and previous_name != "Unknown":
                    previous_name = "Unknown"

            # Object detection and text recognition every frame_divident frames
            if frame_count % frame_divident == 0:
                object_detector.detect_objects(img)
                text_recognizer.recognize_text(img)

            key = cv.waitKey(1)

            if key == ord('1'):
                speak("Reading frame for text", tts.SLOW_VOICE_RATE)
                text_recognizer.recognize_saved_picture(image=img)

            if key == ord('2'):
                audio_handler.start_recording()
                while audio_handler.recording:
                    key = cv.waitKey(1) & 0xFF
                    if key == ord('2'):
                        audio_handler.stop_recording()
                        break

            if key == ord('3'):
                speak("Shutting down...", tts.SLOW_VOICE_RATE)
                break
    except Exception as e:
        print(f"An error occurred: {e}")
        speak(f"An error occurred: {e}", tts.SLOW_VOICE_RATE)
    finally:
        camera.cleanup()
        audio_handler.cleanup()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()
