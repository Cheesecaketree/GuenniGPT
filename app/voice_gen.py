import google.cloud.texttospeech as googleTTs
import elevenlabs
from openai import OpenAI

import os
from central_logger import logger
from app_context import config, primary_tts, fallback_tts


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

def tts_openai(text, filename, language):
    logger.debug("Generating audio with OpenAI")
    
    client = OpenAI(api_key = config['keys']["openai"])

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
    primary_tts.generate_speech(text)
        

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