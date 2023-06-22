import openai
from background_utils import randStr
import remove_emoji
import json
import datetime
import logging
import voice_gen as voice


with open("files/keys.json", "r") as f:
    out = json.load(f)
    
openai.api_key = out["openai"]
openai.organization = out["openai-org"]


def generate_rating(name, language):
    name = name.split("#")[0]
    filename = f"rating_{randStr(N=4)}" + ".mp3"
    
    messages = [
        {
        "role": "system", "content": "You are a discord bot that can talk. You will get names of people and then rate them randomly. Do whatever you want, be creative, be rude. If you want to write \"x/y\" for rating, write it out like \"x out of y\" instead. Keep it short and always use the given language. "
        },
        {
        "role": "user", "content": f"lang={language}; {name} wants to be rated."
        }
    ]
    
    text = get_chatcompletion(messages, temperature=0.93, max_tokens=256)
    voice.generate(text, filename, language)
    
    return filename



def generate_greeting(name, channel, language):
    time_str = datetime.datetime.now().strftime("%H:%M")
    name = name.split("#")[0]
    filename = f"greeting_{randStr(N=4)}" + ".mp3"
    
    system_msg = {
        "role": "system", "content": "You are a discord bot that greets people joining a voice chat. You get passed the name of the person, the time and the server language. Greet them in a funny and creative way. Keep it short, be rude, always use the given language"
    }
    messages = [
        system_msg,
        {"role": "user", "content": f"lang={language}, {name} joined channel \"{channel}\" at {time_str}"},
    ]
    
    text = get_chatcompletion(messages, temperature=1, max_tokens=256)
    
    logging.info(f"Generating greeting for {name} in {channel} with language {language} \n Text: {text}")
    
    voice.generate(text, filename, language)
    
    return filename



def get_chatcompletion(messages, temperature=1, max_tokens=256):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response_message = response.choices[0].message.content
    
    response_message = remove_emoji.remove_emoji(response_message).replace("\"", "")
    
    return response_message


