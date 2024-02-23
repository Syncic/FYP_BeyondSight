import pyttsx3

# Text-To-Speech (TTS)
engine = pyttsx3.init()
speakText = ''


def speak(stext):
    engine.say(stext)
    engine.runAndWait()

