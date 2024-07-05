import tts
import time
from openai import OpenAI


class Commands:
    def __init__(self):
        # Open AI Parameters
        openai_api_key = 'sk-proj-XrJqwYAHtgYNTgEVXTBRT3BlbkFJYFzBVn2rhWe1pYeJW0aZ'
        self.text_client = OpenAI(api_key=openai_api_key)
        
        # General Commands
        self.command_keywords = ['gpt', 'volume', 'time', 'date']
        self.volume_levels = {
            'max': 1.0,
            'full': 1.0,
            'maximum': 1.0,
            'half': 0.5,
            'mid': 0.5,
            'min': 0.15,
            'low': 0.15,
            'minimum': 0.15,
            'high': 0.85,
            'off': 0.0
        }
    
    
    def extract_command(self, extracted_text):
        complete_text = extracted_text.lower()
        print(complete_text)
        
        try:
            command, label = complete_text.split(maxsplit=1)
        except ValueError:
            tts.speak("Invalid command, please read commands documentation or try again...", tts.SLOW_VOICE_RATE)
            return

        print(f"{command}, {label}")
        
        if command not in self.command_keywords:
            tts.speak("Invalid command, please read commands documentation or try again...", tts.SLOW_VOICE_RATE)
            return
        
        if command == 'volume':
            self.volume_adjust(label)
        elif command == 'gpt':
            self.gpt_call(complete_text)
        elif command == 'time':
            self.time_call(label)
        elif command == 'date':
            self.date_call(label)
        else:
            tts.speak("Unknown error, please try again...")

    
    def volume_adjust(self, label: str):
        volume = self.volume_levels.get(label)
        if volume is not None:
            tts.engine.setProperty('volume', volume)
        else:
            tts.speak("Invalid volume level, please try again...", tts.SLOW_VOICE_RATE)

    
    def gpt_call(self, text):
        prompt = f"Answer briefly in 1 or 2 sentences: {text}"
        try:
            response = self.text_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=60,  # Limit the response to a shorter length
                temperature=0.8,  # Optional: Adjust the creativity of the response
                stop=["\n"]  # Optional: You can use a stop sequence to cut off longer responses
            )
            generated_text = response.choices[0].message['content'].strip()
            tts.speak(generated_text)
        except Exception as e:
            print(f"Error: {e}")
            tts.speak("Some unknown error occurred, please try again...", tts.SLOW_VOICE_RATE)

    
    def time_call(self, label):
        if label in ['now', 'current']:
            tts.speak(time.strftime('%I:%M %p'), tts.SLOW_VOICE_RATE)
        else:
            tts.speak("Invalid command, please try again...", tts.SLOW_VOICE_RATE)
            
    
    def date_call(self, label):
        if label in ['now', 'current', 'today']:
            tts.speak(time.strftime('%A, %d %m %Y'), tts.SLOW_VOICE_RATE)
        else:
            tts.speak("Invalid command, please try again...", tts.SLOW_VOICE_RATE)

# Example usage:
# commands = Commands()
# commands.extract_command("gpt tell me a joke")
