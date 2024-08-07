from modules.language_models import LanguageModel, OpenAIChatGPT, GroqChat
from modules.text_to_speech import TextToSpeechEngine, ElevenlabsTTS, OpenAITTS


# TODO implement fallback
# 

class ServiceFactory:
    def create_language_model(self, config):
        llm_service = config['llm']['service']
        model_name = config['llm']['model']
        if llm_service == "OpenAI":
            return OpenAIChatGPT(api_key=config['keys']['openai'], model_name=model_name)
        
        elif llm_service == "Groq":
            return GroqChat(api_key=config['keys']['groq'], model_name=model_name)
    
    def create_text_to_speech_engine(self,config):
        tts_service = config['tts']['service']
        
        tts_model = config['tts']['model']
        tts_voice = config['tts']['voice']
        
        if tts_service == "openai":
            return OpenAITTS(api_key=config['keys']['openai'], model=tts_model, voice=tts_voice)
        elif tts_service == "elevenlabs":
            return ElevenlabsTTS(api_key=config['keys']['elevenlabs'], model=tts_model, voice=tts_voice)