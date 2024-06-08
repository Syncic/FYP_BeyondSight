import pyttsx3

engine = pyttsx3.init()

def Startup():
    newVoiceRate = 200
    engine.setProperty('rate', newVoiceRate)
    engine.setProperty('voice','en-uk-rp')

def speak(text):
    engine.say(text)
    engine.runAndWait()


Startup()