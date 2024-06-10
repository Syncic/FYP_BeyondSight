import wave
import pyaudio
from openai import OpenAI
from tts import speak
import speech_recognition as sr
from voice_commands import Commands
import os


class AudioHandler:
    def __init__(self):
        self.commandHandler = Commands()
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        self.recording = False
        self.frames = []
        self.text_client = OpenAI(api_key='sk-proj-OiNGYm5inInJnuQjM72bT3BlbkFJvYUETrw8VX52fOti4ZaY')

    def start_recording(self):
        speak("recording...")
        print("Recording... Press 'z' again to stop.")
        self.recording = True
        self.frames = []  # Clear frames list before starting a new recording

    def stop_recording(self):
        print("Stopping recording")
        speak("processing...")
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
            self.command_recording(filename=output_filename)
            
    def command_recording(self, filename):
        extractedText = self.process_recording(filename=filename)
        print (extractedText)
        os.remove(filename)
        self.commandHandler.ExtractCommand(extractedText=extractedText)

    def process_recording(self, filename):
         # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Open the audio file
        with open(filename, "rb") as audio_file:
            # Use recognizer to read the audio file
            audio_data = sr.AudioFile(audio_file)
            
            with audio_data as source:
                audio = recognizer.record(source)
            
            # Recognize speech using Google Web Speech API
            try:
                text = ''
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                speak("Could not understand the audio, please try again...")
                return "Could not understand the audio"
            except sr.RequestError:
                speak("Internet Access unavailable, please try later...")
                return "Could not request results from Google Web Speech API"
            except sr.exceptions:
                speak("unknown error occured, please try later")
                return "unknown error occured"

            
        
        
        
        # following is for ai followup
        '''
        with open(filename, "rb") as audio_file:
            translation = self.text_client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
            audio_text = translation.text
        
        print(audio_text)

        
        response = self.text_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": audio_text}]
        )
        generated_text = response.choices[0].message.content
        speak(generated_text)
        '''

    def cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
