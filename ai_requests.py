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


def generate_compliment(name, pLanguage):
    if pLanguage == "de":
        language = "german"
    
    name = name.split("#")[0]
    filename = f"rating_{randStr(N=4)}" + ".mp3"
    
    # orig sys message = "You are a discord bot that can talk. You will get names of people and then rate them randomly. Do whatever you want, be creative, be rude. If you want to write \"x/y\" for rating, write it out like \"x out of y\" instead. Keep it short and always use the given language. "
    system_message = 'You are a discord bot that can talk. You will get the name of a user. Compliment them in a funny and random way. Be creative, be rude. Keep it short. Use the given language'
    user_message = f"Give {name} a compliment.lang={language}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.95, max_tokens=256)
    
    logging.debug(f"Generating compliment for {name} with language {pLanguage} \nText: {text}")
    
    voice.generate(text, filename, pLanguage)
    
    return filename


def generate_rating(name, pLanguage):
    if pLanguage == "de":
        language = "german"
    
    name = name.split("#")[0]
    filename = f"rating_{randStr(N=4)}" + ".mp3"
    
    # orig sys message = "You are a discord bot that can talk. You will get names of people and then rate them randomly. Do whatever you want, be creative, be rude. If you want to write \"x/y\" for rating, write it out like \"x out of y\" instead. Keep it short and always use the given language. "
    system_message = 'You are a discord bot that can talk. You will get the name of a user. Rate them in a funny and random way. Be creative, be rude. For rating on a scale use "x out of y". Keep it short.'
    user_message = f"{name} wants to be rated.lang={language}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.95, max_tokens=256)
    
    logging.debug(f"Generating rating for {name} with language {pLanguage} \nText: {text}")
    
    voice.generate(text, filename, pLanguage)
    
    return filename


def generate_talkAbout(topic, pLanguage):
    if pLanguage == "de":
        language = "german"
    
    filename = f"talkAbout_{randStr(N=4)}" + ".mp3"
    
    # orig sys message = "You are a discord bot that can talk. You will get a topic and then talk about it. Do whatever you want, be creative, be rude. Keep it short and always use the given language. "
    system_message = 'You are a discord bot that can talk. You will get a topic and then talk about it. Be creative. Keep it short.'
    user_message = f"Talk about {topic}.lang={language}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.95, max_tokens=256)
    
    logging.debug(f"Generating talkAbout for {topic} with language {pLanguage} \nText: {text}")
    
    voice.generate(text, filename, pLanguage)
    
    return filename
    
    

def generate_greeting(name, channel, pLanguage, activity):
    language = "german" if pLanguage == "de" else "english"
    time_str = datetime.datetime.now().strftime("%H:%M")
    name = name.split("#")[0]
    filename = f"greeting_{randStr(N=4)}" + ".mp3"
    
    # orig system message: You are a discord bot that greets people joining a voice chat. You get passed the name of the person, the time and the server language. Greet them in a funny and creative way. Keep it short, be rude, always use the given language"
   # original user prompt: f"lang={language}, {name} joined channel \"{channel}\" at {time_str}"
    # f"You are a discord bot that greets people joining a voice channel. You get some information about the user and the channel. Greet them in a funny and creative way. Keep it short, be rude. Dont use emojis. Use this language:{pLanguage}"
    
    system_message = f'You are a discord bot that greets people joining a discord channel. Greet them in a funny and creative way. Keep it to two sentences. Be rude. Use the language:{language}'
    user_message = f'{name} joined channel {channel} at {time_str}.lang={language}'

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.9, max_tokens=256)
    
    logging.debug(f"Generating greeting for {name} in {channel} with language {pLanguage} \nText: {text}")
    
    voice.generate(text, filename, pLanguage)
    
    return filename



def get_chatcompletion(messages, temperature=1, max_tokens=256):
    logging.debug(f"requesting chatcompletion for message: {messages}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response_message = response.choices[0].message.content
    
    response_message = remove_emoji.remove_emoji(response_message).replace("\"", "").replace("\'", "")
    
    return response_message


def moderation_check(message):
    response = openai.Moderation.create(
        input=message,
    )
    output = response["results"][0]
    
    return output
