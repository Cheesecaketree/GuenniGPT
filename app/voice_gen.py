import google.cloud.texttospeech as googleTTs
import elevenlabs
from openai import OpenAI

import os
from central_logger import logger
from config import config, keys


# TODO: implement different TTS services
# TODO: check if quota is exceeded in each service and return error if so (error: "Quota for {service} exceeded")

# TODO: figuere out how to check quota
def tts_google(text, filename, language):
    logger.debug("Generating audio with Google Cloud")

    if not os.path.exists("config/gcloud_key.json"):
        logger.error("Google Cloud credentials not found")
        raise ValueError("Google Cloud credentials not found")

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/gcloud_key.json"

    client = googleTTs.TextToSpeechClient()
    
    mp3_audio_config = googleTTs.AudioConfig(
        audio_encoding=googleTTs.AudioEncoding.MP3,
    )
    
    voice = config["tts"]["google"]["voice"]
    
    input_text = googleTTs.SynthesisInput(text=input)
    
    try:
        response = client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=mp3_audio_config,
        )
    except Exception as e:
        logger.error(f"Error using Google TTS: {e}")
        raise e
    
    return response.audio_content

# TODO: check if quota is checkable (doesnt seem like it, because pay as you go i guess)
def tts_openai(text, filename, language):
    logger.debug("Generating audio with OpenAI")
    
    client = OpenAI(api_key = keys["openai"])

    voice = config["tts"]["openai"]["voice"]
    
    try:
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text
        )
    except Exception as e:
        logger.error(f"Error using OpenAI TTS: {e}")
        raise e
    
    return response


def tts_elevenlabs(text, filename, language):
    logger.debug("Generating audio with Elevenlabs")
    
    elevenlabs.set_api_key(keys["elevenlabs"])
    
    voice = config["tts"]["elevenlabs"]["voice"]
    model = config["tts"]["elevenlabs"]["model"]
    
    # check quota
    import requests
    url = "https://api.elevenlabs.io/v1/user/subscription"
    
    headers = {
        "xi-api-key": keys["elevenlabs"]
    }
    
    quota_response = requests.get(url, headers=headers)
    
    limit = quota_response.json()["character_limit"]
    used = quota_response.json()["character_count"]
    remaining = limit - used
    
    if remaining < len(text):
        logger.error(f"Elevenlabs TTS quota exceeded: {used}/{limit} characters used")
        raise ValueError(f"Elevenlabs TTS quota exceeded: {used}/{limit} characters used")
    
    
    try:
        response = elevenlabs.generate(text=text, voice=voice, model=model)
    except Exception as e:
        logger.error(f"Error using Elevenlabs TTS: {e}")
        raise e
    
    return response  
    
    
def generate_audio(text, filename, language):
    options = {
        "google": tts_google,
        "openai": tts_openai,
        "elevenlabs": tts_elevenlabs
    }
    
    used = ""
    
    # figure out main and falbback service
    # options: google, openai, elevenlabs
    main_service = config["tts"]["main"]
    fallback_service = config["tts"]["fallback"]
    
    if main_service not in options:
        logger.warn(f"Main TTS service {main_service} not supported")
        if fallback_service not in options:
            logger.fatal(f"No valid TTS service configured")
            raise ValueError("No valid TTS service configured")
        
        
    try:
        logger.info(f"Using main TTS service {main_service} to generate audio")
        response = options[main_service](text, filename, language)
        used = main_service
    except Exception as e:
        # main tts failed or quota exceeded, use fallback if available
        logger.error(f"Error using main TTS service {main_service}: {e}")
        
        if fallback_service not in options:
            logger.critical(f"Error using main TTS service {main_service} and no valid fallback service configured")
            raise ValueError(f"Error using main TTS service {main_service} and no valid fallback service configured")
        
        try:
            logger.info(f"Using fallback TTS service {fallback_service} to generate audio")
            response = options[fallback_service](text, filename, language)
            used = fallback_service
        except Exception as e_fallback:
            logger.error(f"Error using fallback TTS service {fallback_service}: {e_fallback}")
            return
        

    if response is not None:
        try:
            if used == "openai":
                response.write_to_file(filename) # couldnt figure out how to make it the same as the other services TODO: look into this because ugly
            else:
                with open(filename, "wb") as out:
                    out.write(response)
                    logger.info(f"Audio content written to file {filename}")
        except Exception as e:
            logger.error(f"Error writing audio content to file {filename}: {e}")
            return 