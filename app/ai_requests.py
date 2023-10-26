import openai
from background_utils import randStr
import remove_emoji
import json
import datetime
import logging
import voice_gen as voice
import random
from config import config

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s| %(message)s', level=logging.WARN)

with open("config/keys.json", "r") as f:
    keys = json.load(f)
    
openai.api_key = keys["openai"]
openai.organization = keys["openai-org"]


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
    filename = f"greeting_{randStr(N=4)}" + ".mp3"
    language = "german" if pLanguage == "de" else "english" # TODO: implement different languages properly
    
    username = str(user).split("#")[0] # shouldn"t be necessary anymore since discord changed usernames, needs testing
    time_str = datetime.datetime.now().strftime("%H:%M")
    activity = user.activity # TODO: Find out what permissions are needed for this (audit log maybe?)
    num_other_people = len(channel.members) - 1
    
    event = get_random_event_today()
    style = get_random_greeting_style()
    
    # weighted additions to the prompt
    additions = [
        {"weight": 2, "text": f"There are currently {num_other_people} other people in the channel."},
        {"weight": 1, "text": f"The channel is called {channel.name}."},
        {"weight": 1, "text": f"The channel is called {channel.name} and there are {num_other_people} other people present."},
        {"weight": 2, "text": f"Today is {datetime.datetime.now().strftime('%A')}."},
    ]

    additions.append({"weight": 3, "text": f"They are currently alone in the channel"}) if num_other_people == 0 else None
    additions.append({"weight": 6, "text": f"{event}"}) if event else None
    additions.append({"weight": 5, "text": f"{username} is currently playing {activity}."}) if activity else None
    
    # choose a random addition based on the weights
    addition = random.choices(additions, weights=[entry["weight"] for entry in additions], k=1)[0]["text"]
    
    sys_message = f"Generate a {style} greeting for someone who just joined the Discord voice channel in at most three sentences. Only answer in {language} and keep it short."
    usr_message = f"{username} joined at {time_str}. {addition}"

    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": usr_message},
    ]
    
    try:
        text = get_chatcompletion(messages, temperature=1, max_tokens=256)
        logging.debug(f"generated greeting text: {text}")
    except Exception as e:
        # if something goes wrong, just use a default message, kinda boring but better than nothing
        # not even sure if this can happen, but better safe than sorry
        logging.error(f"Error generating chat completion: {e}")
        text = f"Hey {username}!"
    
    voice.generate(text, filename, pLanguage)
    
    return filename

# Returns a random greeting style from the config
def get_random_greeting_style():
    styles = config["greeting_styles"]
    return random.choices(list(styles.keys()), weights=[styles[entry] for entry in styles])[0]  

# returns all events for today if there are any
def get_random_event_today():
    return random.choice(config["events"][datetime.datetime.now().strftime("%d.%m")]) if datetime.datetime.now().strftime("%d.%m") in config["events"] else None


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
