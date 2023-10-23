import openai
from background_utils import randStr
import remove_emoji
import json
import datetime
import logging
import voice_gen as voice
import random

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s| %(message)s', level=logging.WARN)

with open("config/keys.json", "r") as f:
    out = json.load(f)
    
openai.api_key = out["openai"]
openai.organization = out["openai-org"]


def generate_compliment(name, pLanguage):
    if pLanguage == "de":
        language = "german"
    
    name = name.split("#")[0]
    filename = f"rating_{randStr(N=4)}" + ".mp3"
    
    system_message = "You are a discord bot that can talk. You will get the name of a user. Compliment them in a funny and random way. Be creative, be rude. Keep it short. Use the given language"
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
    
    system_message = "You are a discord bot that can talk. You will get the name of a user. Rate them in a funny and random way. Be creative, be rude. For rating on a scale use 'x out of y'. Keep it short."
    user_message = f"{name} wants to be rated.lang={language}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.95, max_tokens=256)
    
    logging.debug(f"Generating rating for {name} with language {pLanguage} \nText: {text}")
    
    voice.generate(text, filename, pLanguage)
    
    return filename

# TODO: implement feature or delete this function
def generate_talkAbout(topic, pLanguage):
    if pLanguage == "de":
        language = "german"
    
    filename = f"talkAbout_{randStr(N=4)}" + ".mp3"
    
    # orig sys message = "You are a discord bot that can talk. You will get a topic and then talk about it. Do whatever you want, be creative, be rude. Keep it short and always use the given language. "
    system_message = f"You are a discord bot that can talk. You will get a topic and then talk about it. Be creative. Keep it short."
    user_message = f"Talk about {topic}.lang={language}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.95, max_tokens=256)
    
    logging.debug(f"Generating talkAbout for {topic} with language {pLanguage} \nText: {text}")
    
    voice.generate(text, filename, pLanguage)
    
    return filename
    
    
# TODO: implement new prompt and more data for the prompts to work with
def generate_greeting(user, channel, pLanguage):
    channel.name
    filename = f"greeting_{randStr(N=4)}" + ".mp3"
    name = str(user).split("#")[0] # shouldn"t be necessary anymore since discord changed usernames, but doenst break anything like this
    language = "german" if pLanguage == "de" else "english" # TODO: implement differnt languages properly
    
    time_str = datetime.datetime.now().strftime("%H:%M")
    activity = user.activity # TODO: Find out what permissions are needed for this (audit log maybe??)
    other_people = len(channel.members) - 1 # TODO: needs testing! 
    
    
   
    extra_info = [
        {"weight": 2, "text": f"There are currently {other_people} other people in the channel."}, # other people
        {"weight": 1, "text": f"The channel is called {channel.name}."}, # channel name
        {"weight": 1, "text": f"The channel is called {channel.name} and there are {other_people} other people present."}, # channel name
        {"weight": 2, "text": f"Today is {datetime.datetime.now().strftime('%A')}."}, # Day of week
        {"weight": 100, "text": f"Their current activity is {activity}"}, 
    ]
        
    
    events = get_events_today()
    event = ""
    if len(events) > 0:
        event = random.choice(events)
        event_dict = {"weight": 4, "text": f"{event}"}
        extra_info.append(event_dict)
        logging.info(f"event: {event} added to extra_info")
    
    
    weights = [entry["weight"] for entry in extra_info]
    chosen_entry = random.choices(extra_info, weights=weights, k=1)[0]
    chosen_entry_text = chosen_entry["text"]
    
    sys_message = f"You are GuenniGPT, a discord bot that greets people when they join a voice channel. You will be provided with some information on the person and channel. Generate a funny, sarcastic or a rude greeting for them. Only answer in {language}, keep the answer short, at most three sentences."
    usr_message = f"{name} joined at {time_str}. {chosen_entry_text}"

    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": usr_message},
    ]
    
    try:
        text = get_chatcompletion(messages, temperature=1, max_tokens=256)
        logging.debug(f"generated greeting text: {text}")
    except Exception as e:
        logging.error(f"Error generating chat completion: {e}")
        text = f"Hey {name}!"
    
    voice.generate(text, filename, pLanguage)
    
    return filename


def get_events_today():
    events = []
    with open("config/events.json", "r") as f:
        events = json.load(f)
    
    # get all entries for the current day
    # date is key value in format dd.mm
    today = datetime.datetime.now().strftime("%d.%m")
    
    if today not in events:
        return []
    
    return events[today]

def get_chatcompletion(messages, temperature=1, max_tokens=256):
    logging.debug(f"requesting chatcompletion for message: {messages}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response_message = response.choices[0].message.content
    response_message = remove_emoji.remove_emoji(response_message).replace('\"', '').replace('\"', '')
    return response_message


# Dont know why this is here, not used anywhere
def perform_moderation_check(text_to_check):
    response = openai.Moderation.create(
        input=text_to_check,
    )
    output = response["results"][0]
    
    return output
