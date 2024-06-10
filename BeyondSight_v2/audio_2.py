# audio.py

import wave
import pyaudio
from openai import OpenAI
from tts import speak

class AudioHandler:
    def __init__(self):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.frames = []
        self.text_client = OpenAI(api_key='sk-proj-OiNGYm5inInJnuQjM72bT3BlbkFJvYUETrw8VX52fOti4ZaY')

    def start_recording(self):
        if self.recording:
            return  # Prevent multiple recordings at the same time

        speak("recording...")
        print("Recording... Press 'z' again to stop.")
        self.recording = True
        self.frames = []  # Reset frames list
        self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        
        while self.recording:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
            except Exception as e:
                print(f"Error while recording: {e}")
                self.recording = False
                self.cleanup()
                break

    def stop_recording(self):
        if not self.recording:
            return  # No recording to stop

        print("Stopping recording")
        self.recording = False
        self.save_recording()

    def save_recording(self):
        if self.frames:
            output_filename = "Recorded.wav"
            wf = wave.open(output_filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            print("Recording saved as Recorded.wav")
            self.process_recording(output_filename)

    def process_recording(self, filename):
        with open(filename, "rb") as audio_file:
            translation = self.text_client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
            audio_text = translation.text

        response = self.text_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": audio_text}]
        )
        generated_text = response.choices[0].message.content
        speak(generated_text)

    def cleanup(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
