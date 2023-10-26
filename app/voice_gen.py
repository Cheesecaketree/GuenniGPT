import google.cloud.texttospeech as tts
import os
import logging
from gtts import gTTS

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/gcloud_key.json"

def synthesize_ssml(input, voice, audio_config):
    client = tts.TextToSpeechClient()
    
    input_text = tts.SynthesisInput(text=input)
    
    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )
    
    return response, input_text

# TODO: implement language change
de_voice = tts.VoiceSelectionParams(
    language_code="de-DE", # "de-DE",
    name= "de-DE-Standard-F",   # "de-DE-Standard-F", #"de-DE-Wavenet-F", 
    ssml_gender=tts.SsmlVoiceGender.FEMALE,
)

mp3_audio_config = tts.AudioConfig(
    audio_encoding=tts.AudioEncoding.MP3,
)



def generate(text, filename, language):
    logging.debug("Generating audio with Google Cloud")
    voice = tts.VoiceSelectionParams(
        language_code=language,
        ssml_gender=tts.SsmlVoiceGender.FEMALE,
    )
    
    response, input_text = synthesize_ssml(text, voice, mp3_audio_config)
    
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        logging.info(f"Audio content written to file {filename}")
    
    
def generate_gtts(pText, filename, language): 
    logging.debug("Generating audio with gTTs")
    nachricht = gTTS(text=pText, lang=language, slow=False)
    filename = filename
    nachricht.save(filename)
    logging.info(f"Audio content written to file {filename}")