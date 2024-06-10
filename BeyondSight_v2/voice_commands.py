import tts
from openai import OpenAI


class Commands:
    def __init__(self):
        # Open AI Parameters
        self.text_client = OpenAI(api_key='sk-proj-OiNGYm5inInJnuQjM72bT3BlbkFJvYUETrw8VX52fOti4ZaY')
        
        # General Commands
        self.commandKeywords = ['gpt', 'volume']
    
    def ExtractCommand(self, extractedText):
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
        response = self.text_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        
        generated_text = response.choices[0].message.content
        tts.speak(generated_text)
