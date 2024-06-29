import tts
import time
from openai import OpenAI


class Commands:
    def __init__(self):
        # Open AI Parameters
        self.text_client = OpenAI(api_key='sk-proj-OiNGYm5inInJnuQjM72bT3BlbkFJvYUETrw8VX52fOti4ZaY')
        
        # General Commands
        self.commandKeywords = ['gpt', 'volume', 'time', 'date']
    
    
    def ExtractCommand(self, extractedText):
        try:
            completeText = extractedText.lower()
            print(completeText)
            words = completeText.split()
            command = words[0]
            label = words[1]
            print(f"{command}, {label}")
            
            if command not in self.commandKeywords:
                tts.speak("invalid command, please read commands documentation or try again...", tts.SLOW_VOICE_RATE)
            
            else:
                if command == 'volume':
                    self.VolumeAdjust(label=label)
                elif command == 'gpt':
                    self.GptCall(text=completeText)
                elif command == 'time':
                    self.TimeCall(label=label)
                elif command == 'date':
                    self.DateCall(label=label)
        except:
            tts.speak("unknown error, please try again...")
        
    
    def VolumeAdjust(self, label : str):
        if label == 'max' or label == 'full' or label == 'maximum':
            tts.engine.setProperty('volume', 1.0)
        elif label == 'half' or label == 'mid':
            tts.engine.setProperty('volume', 0.5)
        elif label == 'min' or label == 'low' or label == 'minimum':
            tts.engine.setProperty('volume', 0.15)
        elif label == 'high':
            tts.engine.setProperty('volume', 0.85)
        elif label == 'off':
            tts.engine.setProperty('volume', 0.0)
        else:
            pass
        
    
    def GptCall(self, text):
        try:
            response = self.text_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}]
            )
            
            generated_text = response.choices[0].message.content
            tts.speak(generated_text)
        except:
            tts.speak('some unknown error occured, please try again...', tts.SLOW_VOICE_RATE)
    
    def TimeCall(self, label):
        if label == 'now' or label == 'current':
            tts.speak(time.strftime('%I:%M %p'),tts.SLOW_VOICE_RATE)
        else:
            tts.speak('invalid command, please try again...')
            
    
    def DateCall(self, label):
        if label == 'now' or label == 'current' or label == 'today':
            tts.speak(time.strftime('%A, %d %m %Y'),tts.SLOW_VOICE_RATE)
        else:
            tts.speak('invalid command, please try again...')