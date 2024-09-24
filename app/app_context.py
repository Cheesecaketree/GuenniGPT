import json
import tomllib

def load_config():
    with open('config/config.toml', mode="rb") as f:
        config = tomllib.load(f)
        
    keys = load_keys()
    config['keys'] = keys
    return config

def load_keys():
    with open('config/keys.toml', mode="rb") as f:
        keys = tomllib.load(f)
    return keys

config = load_config()



from modules.service_factory import ServiceFactory
    
# TODO implement fallback
factory = ServiceFactory()
primary_llm = factory.create_language_model(load_config())

primary_tts = factory.create_text_to_speech_engine(load_config())
fallback_tts = NotImplemented
