import pyttsx3

engine = pyttsx3.init()

# CONSTANTS
SLOW_VOICE_RATE = 170
FAST_VOICE_RATE = 200

def Startup():
    
    engine.setProperty('voice','en-uk-rp')

Startup()

def speak(text, voiceRate = 200):
    newVoiceRate = voiceRate
    engine.setProperty('rate', newVoiceRate)
    engine.say(text)
    engine.runAndWait()

