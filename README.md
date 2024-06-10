# BeyondSight: A real-time Navigational Aid for the Visually impaired

---

## Overview
This project is a comprehensive Navigational Aid System that integrates various functionalities such as object detection, text recognition, and voice commands to assist users in navigation. The system uses computer vision techniques to detect objects and recognize text, and it utilizes text-to-speech (TTS) to provide audio feedback to the user. The system can also process voice commands to control its functionalities.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Modules](#modules)
    - [main.py](#mainpy)
    - [camera.py](#camerapy)
    - [audio.py](#audiopy)
    - [object_detection.py](#object_detectionpy)
    - [text_recognition.py](#text_recognitionpy)
    - [tts.py](#ttspy)
    - [utils.py](#utilspy)
    - [voice_commands.py](#voice_commandspy)
4. [Contributing](#contributing)
5. [License](#license)

## Installation

### Prerequisites
Ensure you have the following dependencies installed:
- Python 3.8 or higher
- OpenCV
- pyttsx3
- pyaudio
- SpeechRecognition
- pytesseract
- ultralytics

### Clone the Repository
```sh
git clone https://github.com/yourusername/navigational-aid-system.git
cd navigational-aid-system
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Setup Tesseract
Ensure Tesseract is installed on your system. You can download it from [here](https://github.com/tesseract-ocr/tesseract).

## Usage
Run the main script to start the Navigational Aid System:
```sh
python main.py
```
The system will initialize the camera and audio handler, and start detecting objects and recognizing text. Use the following keys for interactions:
- `p`: Read frame for text
- `z`: Start/stop recording audio
- `q`: Shutdown the system

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
## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---
## Contact
For any inquiries, please reach out to umerzubairi@hotmail.com.
