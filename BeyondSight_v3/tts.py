import pyttsx3

# CONSTANTS
SLOW_VOICE_RATE = 170
FAST_VOICE_RATE = 200

# Initialize and configure the engine
engine = pyttsx3.init()
engine.setProperty('voice', 'en-uk-rp')

def speak(text, voice_rate=FAST_VOICE_RATE):
    engine.setProperty('rate', voice_rate)
    engine.say(text)
    engine.runAndWait()

# Example usage:
# speak("Hello, how are you?", SLOW_VOICE_RATE)


