import wave
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from openai import OpenAI
from tts import speak
from voice_commands import Commands
import os
import threading


class AudioHandler:
    def __init__(self):
        self.command_handler = Commands()
        self.samplerate = 44100
        self.channels = 1
        self.dtype = 'int16'
        self.frames = []
        self.recording = False
        self.text_client = OpenAI(api_key='sk-proj-OiNGYm5inInJnuQjM72bT3BlbkFJvYUETrw8VX52fOti4ZaY')

    def start_recording(self):
        """Start audio recording."""
        speak("Recording...")
        print("Recording... Press 'z' again to stop.")
        self.recording = True
        self.frames = []
        self.stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=self._callback)
        self.stream.start()
        threading.Thread(target=self._record_audio).start()

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.frames.append(indata.copy())

    def _record_audio(self):
        while self.recording:
            sd.sleep(100)  # Sleep for 100 ms to yield control

    def stop_recording(self):
        """Stop audio recording and process the recorded data."""
        print("Stopping recording")
        speak("Processing...")
        self.recording = False
        self.stream.stop()
        self.stream.close()
        threading.Thread(target=self._process_and_execute).start()

    def _process_and_execute(self):
        """Process the recorded audio and execute the recognized command."""
        output_filename = "Recorded.wav"
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(np.dtype(self.dtype).itemsize)
            wf.setframerate(self.samplerate)
            wf.writeframes(b''.join(self.frames))
        print("Recording saved as Recorded.wav")
        self.process_and_execute_command(output_filename)
        os.remove(output_filename)

    def process_and_execute_command(self, filename):
        """Process the recorded audio and execute the recognized command."""
        extracted_text = self.transcribe_audio(filename)
        self.command_handler.extract_command(extracted_text)

    def transcribe_audio(self, filename):
        """Transcribe audio from a WAV file to text."""
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                speak("Could not understand the audio, please try again...")
                return "Could not understand the audio"
            except sr.RequestError:
                speak("Internet access is needed for speech understanding, please try later...")
                return "Could not request results from Google Web Speech API"
            except Exception as e:
                speak(f"An error occurred: {str(e)}")
                return "An unknown error occurred"

    def cleanup(self):
        """Clean up resources."""
        pass  # No specific cleanup required for sounddevice


# Example usage:
# audio_handler = AudioHandler()
# audio_handler.start_recording()
# (Press 'z' to stop recording)
# audio_handler.stop_recording()
# audio_handler.cleanup()
