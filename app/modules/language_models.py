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
        
        return response.choices[0].message.content
        

# Groq has access to multiple llama models, mixtral 8x7b and google gemma models
# Price is very low and speed is full insanity
class GroqChat(LanguageModel): 
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

        return response.choices[0].message.content
        
        
    
    
    