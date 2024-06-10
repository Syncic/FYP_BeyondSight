import pyttsx3

engine = pyttsx3.init()

def Startup():
    
    engine.setProperty('voice','en-uk-rp')

Startup()

def speak(text, voiceRate = 200):
    newVoiceRate = voiceRate
    engine.setProperty('rate', newVoiceRate)
    engine.say(text)
    engine.runAndWait()

