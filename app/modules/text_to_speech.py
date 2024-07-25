from abc import ABC, abstractmethod
from openai import OpenAI
from elevenlabs.client import ElevenLabs
import io

# Abstract Class for LLM
class TextToSpeechEngine():
    @abstractmethod
    def generate_speech(self, text: str, **kwargs) -> str:
        """Generates text based on given prompt."""
        

class OpenAITTS(TextToSpeechEngine):
    def __init__(self, api_key: str, voice: str, model: str = "tts-1"):
        self.client = OpenAI(api_key = api_key)
        
        self.voice = voice
        self.model = model
        
    def generate_speech(self, input: str, **kwargs) -> str:
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=input
            )
        except Exception as e:
            
            raise e
    
        audio_data = response.content
    
        return audio_data


class ElevenlabsTTS(TextToSpeechEngine):
    def __init__(self, api_key: str, voice: str, model: str):
        
        self.client = ElevenLabs(api_key=api_key)
        self.key = api_key
        self.voice = voice
        self.model = model
        
    def check_quota(self, text):
        # check quota
        import requests
        url = "https://api.elevenlabs.io/v1/user/subscription"
        
        headers = {
            "xi-api-key": self.key
        }
        
        quota_response = requests.get(url, headers=headers)
        
        limit = quota_response.json()["character_limit"]
        used = quota_response.json()["character_count"]
        remaining = limit - used
        
        if remaining < len(text):
            
            raise ValueError(f"Elevenlabs TTS quota exceeded: {used}/{limit} characters used")
        
        
        
    def generate_speech(self, input: str, **kwargs) -> str:
        self.check_quota(input)
        
        try:
            response = self.client.text_to_speech.convert(
                text=input,
                output_format="mp3_22050_32",
                voice_id=self.voice,
                model_id=self.model,
            )
            
        except Exception as e:
            
            raise e
    
        audio_stream = io.BytesIO()
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)
                
        audio_stream.seek(0)
    
        return audio_stream
        
    
    
        