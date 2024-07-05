import pyttsx3

# Constants
SLOW_VOICE_RATE = 170
FAST_VOICE_RATE = 200

# Initialize and configure the engine once
engine = pyttsx3.init()
engine.setProperty('voice', 'en-uk-rp')
engine.setProperty('rate', FAST_VOICE_RATE)  # Set default rate

def speak(text, voice_rate=FAST_VOICE_RATE):
    engine.setProperty('rate', voice_rate)
    engine.say(text)
    engine.runAndWait()

# Example usage:
# speak("Hello, how are you?", SLOW_VOICE_RATE)
# speak("Hello, how are you?")  # Uses default FAST_VOICE_RATE




