from abc import ABC, abstractmethod
from openai import OpenAI
import elevenlabs
from central_logger import logger
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
            logger.error(f"Error using OpenAI TTS: {e}")
            raise e
    
        audio_data = response.content
    
        return audio_data


class ElevenlabsTTS(TextToSpeechEngine):
    def __init__(self, api_key: str, voice: str, model: str):
        elevenlabs.set_api_key(api_key=api_key)
        
        self.key = api_key
        self.voice = voice
        self.model = model
        
    def check_quota(self):
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
        
        if remaining < len(self.input):
            logger.error(f"Elevenlabs TTS quota exceeded: {used}/{limit} characters used")
            raise ValueError(f"Elevenlabs TTS quota exceeded: {used}/{limit} characters used")
        
        
        
    def generate_speech(self, input: str, **kwargs) -> str:
        self.check_quota()
        
        try:
            response = elevenlabs.generate(text=input, voice=self.voice, model=self.model)
        except Exception as e:
            logger.error(f"Error using Elevenlabs TTS: {e}")
            raise e
    
        audio_stream = io.BytesIO()
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)
                
        audio_stream.seek(0)
    
        return audio_stream
        
    
    
        