# BeyondSight: A real-time Navigational Aid for the Visually impaired

### Project: Tecto - Your Navigational Aid

---

#### Overview
Tecto is an advanced navigational aid designed to assist users by detecting objects, recognizing text, and responding to voice commands. It leverages computer vision, speech recognition, and text-to-speech technologies to provide an interactive and intuitive user experience.

#### Repository Structure
The project is organized into several modules, each responsible for specific functionalities:

1. **main.py**: The central script that integrates all modules and coordinates their operations.
2. **camera.py**: Handles camera operations including capturing frames and saving pictures.
3. **audio.py**: Manages audio recording, processing, and interaction with voice commands.
4. **object_detection.py**: Implements object detection using YOLO (You Only Look Once) model.
5. **text_recognition.py**: Facilitates text recognition from images using Tesseract OCR.
6. **tts.py**: Provides text-to-speech functionality.
7. **utils.py**: Contains utility functions used across the project.
8. **voice_commands.py**: Processes and executes voice commands.

---

### Detailed Module Documentation

#### main.py

**Description:**
The `main.py` script is the entry point of the application. It initializes the camera, audio handler, object detector, and text recognizer modules. It then enters a loop to continuously capture frames, detect objects, and recognize text.

**Key Functions:**
- **speak()**: Provides auditory feedback to the user.
- **Camera.get_frame()**: Captures a frame from the camera.
- **ObjectDetector.detect_objects()**: Detects objects in the frame.
- **TextRecognizer.recognize_text()**: Recognizes text in the frame.
- **AudioHandler.start_recording() / stop_recording()**: Handles audio recording.

**Usage:**
```python
python main.py
```

#### camera.py

**Description:**
This module manages the camera operations.

**Class:**
- **Camera**: Initializes the camera, captures frames, and saves pictures.

**Methods:**
- **get_frame()**: Captures a frame from the camera.
- **save_picture()**: Saves the captured frame to a file.
- **cleanup()**: Releases the camera resource.

**Usage:**
```python
camera = Camera()
ret, img = camera.get_frame()
camera.save_picture(img)
camera.cleanup()
```

#### audio.py

**Description:**
Handles audio recording, speech recognition, and executing voice commands.

**Class:**
- **AudioHandler**: Manages audio recording and processing.

**Methods:**
- **start_recording()**: Starts audio recording.
- **stop_recording()**: Stops audio recording and processes the recording.
- **save_recording()**: Saves the audio recording to a file.
- **command_recording()**: Extracts and executes commands from the audio.
- **process_recording()**: Processes the recorded audio to extract text.
- **cleanup()**: Cleans up audio resources.

**Usage:**
```python
audio_handler = AudioHandler()
audio_handler.start_recording()
audio_handler.stop_recording()
audio_handler.cleanup()
```

#### object_detection.py

**Description:**
This module detects objects in the captured frames using YOLO model.

**Class:**
- **ObjectDetector**: Detects objects and announces their presence.

**Methods:**
- **detect_objects()**: Detects objects in the frame and announces their location.

**Usage:**
```python
object_detector = ObjectDetector()
object_detector.detect_objects(img)
```

#### text_recognition.py

**Description:**
Handles text recognition from images using Tesseract OCR.

**Class:**
- **TextRecognizer**: Recognizes text and checks for specific keywords.

**Methods:**
- **recognize_text()**: Recognizes text in the frame and announces detected keywords.
- **recognize_saved_picture()**: Recognizes text in a saved picture.

**Usage:**
```python
text_recognizer = TextRecognizer()
text_recognizer.recognize_text(img)
text_recognizer.recognize_saved_picture(image)
```

#### tts.py

**Description:**
Provides text-to-speech capabilities.

**Functions:**
- **speak()**: Converts text to speech at a specified voice rate.
- **Startup()**: Initializes the TTS engine with default settings.

**Usage:**
```python
speak("Hello! I am Tecto, your Navigational Aid")
```

#### utils.py

**Description:**
Contains utility functions used for object detection and localization.

**Functions:**
- **get_center()**: Computes the center of a bounding box.
- **get_location()**: Determines the location (left, center, right) of an object based on its center.

**Usage:**
```python
center = get_center(box)
location = get_location(center, width, height)
```

#### voice_commands.py

**Description:**
Processes voice commands and interacts with OpenAI's GPT-3.5 for responses.

**Class:**
- **Commands**: Handles voice commands and interacts with OpenAI's API.

**Methods:**
- **ExtractCommand()**: Extracts and executes commands from the text.
- **VolumeAdjust()**: Adjusts the volume based on the command.
- **GptCall()**: Interacts with OpenAI's API for generating responses.

**Usage:**
```python
commandHandler = Commands()
commandHandler.ExtractCommand(extractedText)
```

---

### Getting Started

**Installation:**
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/tecto-navigational-aid.git
   cd tecto-navigational-aid
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

**Running the Application:**
```sh
python main.py
```

---

### Contribution

Contributions are welcome! Please read the [contributing guide](CONTRIBUTING.md) for more details.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Contact

For any inquiries, please reach out to [your-email@example.com](mailto:your-email@example.com).
