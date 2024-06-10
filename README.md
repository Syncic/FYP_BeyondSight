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
- Python 3.7 or higher
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

## Modules

### main.py
This is the entry point of the system. It initializes the camera, audio handler, object detector, and text recognizer modules. It handles the main loop for capturing frames, processing objects and text, and managing voice commands.

### camera.py
This module handles the camera operations.
- **Camera**: Class for capturing frames from the camera and saving pictures.

### audio.py
This module handles audio recording and processing.
- **AudioHandler**: Class for recording audio, saving recordings, and processing them using speech recognition.

### object_detection.py
This module performs object detection using the YOLO model.
- **ObjectDetector**: Class for detecting objects in the captured frames and providing audio feedback.

### text_recognition.py
This module performs text recognition using Tesseract.
- **TextRecognizer**: Class for recognizing text in the captured frames and providing audio feedback.

### tts.py
This module handles text-to-speech operations.
- **speak**: Function for converting text to speech using pyttsx3.
- **SLOW_VOICE_RATE**, **FAST_VOICE_RATE**: Constants for controlling the speed of speech.

### utils.py
This module contains utility functions for the system.
- **get_center**: Function to calculate the center of a bounding box.
- **get_location**: Function to determine the location of an object within the frame.

### voice_commands.py
This module processes voice commands and performs corresponding actions.
- **Commands**: Class for handling voice commands and interfacing with OpenAI for advanced processing.

## Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to customize this documentation further to suit your project's specific needs. Let me know if there's anything more you'd like to add or modify!
