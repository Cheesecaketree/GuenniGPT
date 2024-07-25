import openai
from background_utils import randStr
import remove_emoji
import datetime
import random
from app_context import config, primary_llm, primary_tts

from central_logger import logger
    
openai.api_key = config['keys']["openai"]
openai.organization = config['keys']["openai-org"]


def generate_compliment(name):
    language = config["language"]
    
    name = name.split("#")[0]
    filename = f"rating_{randStr(N=4)}" + ".mp3"
    
    system_message = "You are a discord bot that can talk. You will get the name of a user. Compliment them in a funny and random way. Be creative, be rude. Keep it short. Use the given language"
    user_message = f"Give {name} a compliment.lang={language}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.95, max_tokens=256)
    
    logger.debug(f"Generating compliment for {name} with language {language} \nText: {text}")
    
    voice.generate_audio(text, filename, language)
    
    return filename

def generate_rating(name):
    language = config["language"]
    
    name = name.split("#")[0]
    filename = f"rating_{randStr(N=4)}" + ".mp3"
    
    system_message = "You are a discord bot that can talk. You will get the name of a user. Rate them in a funny and random way. Be creative, be rude. For rating on a scale use 'x out of y'. Keep it short."
    user_message = f"{name} wants to be rated.lang={language}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    
    text = get_chatcompletion(messages, temperature=0.95, max_tokens=256)
    
    logger.debug(f"Generating rating for {name} with language {language} \nText: {text}")
    
    voice.generate_audio(text, filename, language)
    
    return filename
    
    
def generate_greeting(user, channel):
    language = config["language"]
    
    prompt_config = config['greeting_prompt']
    additions = prompt_config['additions']
    
    username = str(user).split("#")[0] if not type(user) == str else user 
    
    time_format = prompt_config['time_format']
    date_format = prompt_config['date_format']
    time_str = datetime.datetime.now().strftime(time_format) 
    date = datetime.datetime.now().strftime(date_format)
    
    
    activity = None
    if not type(user) == str:
        activity = user.activity if user.activity else None
        
    num_other_people = len(channel.members) - 1 
    
    event = get_random_event_today() if config['events']['use_events'] else ""
    style = get_random_greeting_style()
  
    
    other_people_text = additions['other_people_text'].format(num_other_people=num_other_people)
    activity_text = additions['activity_text'].format(activity=activity) if activity else ""
    
    
    sys_prompt = prompt_config['system'].format(date=date, time=time_str, language=language)
    usr_prompt = prompt_config['user'].format(
        username=username,
        channelname=channel,
        style=style,
        activity = activity_text,
        event=event,
        other_people=other_people_text
        )

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": usr_prompt},
    ]
    
    try:
        text = primary_llm.generate_text(messages, max_tokens=1024)
        text = remove_emoji(text)

    
    except Exception as e:
        # if something goes wrong, just use a default message, kinda boring but better than nothing
        logger.error(f"Error generating chat completion: {e}")
        text = f"Hey {username}!"
    
    file = primary_tts.generate_speech(text)
    
    return file

# Returns a random greeting style from the config
def get_random_greeting_style():
    styles = config["greeting_prompt"]['styles']
    return random.choices(list(styles.keys()), weights=[styles[entry] for entry in styles])[0]  

# returns all events for today if there are any
def get_random_event_today():
    return random.choice(config["events"][datetime.datetime.now().strftime("%d.%m")]) if datetime.datetime.now().strftime("%d.%m") in config["events"] else None

# Wishes the user a good night
def generate_good_night(user):
    language = config["language"]
    filename = f"good_night_{randStr(N=4)}" + ".mp3"
    
    name = user.name
    styles = ["funny", "creative", "poetic"]
    
    
    sys_message = f"Wish a person in a Discord voice channel a good night. Be {random.choices(styles)}. Always answer in {language} and keep it under three sentences."
    usr_message = f"Wish {name} a good night."
    
    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": usr_message},
    ]
    
    text = get_chatcompletion(messages, temperature=1, max_tokens=256)
    logger.debug(f"generated greeting text: {text}")
    
    voice.generate_audio(text, filename, language)
    
    return filename
    

def get_chatcompletion(messages, temperature=1, max_tokens=256):
    logger.debug(f"requesting chatcompletion for message: {messages}")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response_message = response.choices[0].message.content
    response_message = remove_emoji.remove_emoji(response_message).replace('\"', '').replace('\"', '')
    return response_message

