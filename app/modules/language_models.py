from abc import ABC, abstractmethod
from openai import OpenAI
from groq import Groq

# Abstract Class for LLM
class LanguageModel():
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generates text based on given prompt."""
        
    
    
class OpenAIChatGPT(LanguageModel):
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        self.model = model_name
        self.client = OpenAI(api_key=api_key)
        
    def generate_text(self, prompt: str, temperature: int = 1, max_tokens: int = 512, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            messages=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False
        )
        
        # TODO add cleanup (remove emojis?)
        
        return response.choices[0].message.content
        
        
        
        


# Groq has access to multiple llama models, mixtral 8x7b and google gemma models
# Price is very low and speed is full insanity
class GroqChat(LanguageModel):
    """
    Tested prompt example for llama-3.1-70b-versatile
    
    system:
You are a Discord Bot that greets people when they enter a voice channel. Only answer in German.
Stick to the instructions!
Your purpose is to make the experience in the voice channel more fun. Answer in roughly 4 sentences.
Today is {Thursday, 25.07.2024}. It is currently {00:44 AM}
    
    User:
    Generate a {STYLE} greeting for "{USERNAME}" who just entered the Discord voice channel "{channelname}".
    They are currently the only one in the channel. It is 01:23 AM on thursday. Their current discord activity is "{DISCORD ACTIVITY}".
    
    tested styles with good results:
    very formal, sad but funny, sad, sarcastic, formal, confused
    
    """
    
    
    def __init__(self, api_key: str, model_name: str):
        self.client = Groq(api_key=api_key)
        self.model_name = model_name
        
    def generate_text(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt,
            temperature=1,
            max_tokens= 2048,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        # TODO add text cleanup?
        return response.choices[0].message.content
        
        
    
    
    