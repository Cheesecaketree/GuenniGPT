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
    
    prompt_config = config['compliment_prompt']
    
    name = name.split("#")[0]
    
    sys_prompt = prompt_config['system']
    usr_prompt = prompt_config['user']
    sys_prompt = sys_prompt.format(language=language)
    usr_prompt = usr_prompt.format(name=name)
    
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": usr_prompt},
    ]
    
    text = primary_llm.generate_text(messages, max_tokens=256, temperature=0.95)
    text = text_cleanup(text)
    
    
    logger.debug(f"Generating compliment for {name} with language {language} \nText: {text}")
    
    file_path = primary_tts.generate_speech(text)
    
    return file_path

def generate_rating(name):
    language = config["language"]
    
    prompt_config = config['rating_prompt']
    
    name = name.split("#")[0]
    
    
    sys_prompt = prompt_config['system']
    usr_prompt = prompt_config['user']
    sys_prompt = sys_prompt.format(language=language)
    usr_prompt = usr_prompt.format(name=name)
    
      
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": usr_prompt},
    ]
    
    text = primary_llm.generate_text(messages, max_tokens=256, temperature=0.95)
    text = text_cleanup(text)
    
    file_path = primary_tts.generate_speech(text)
    
    return file_path
    
    
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
        
    num_people_in_channel = len(channel.members) # total number of people in the channel, including the newly joined user
    
    event = get_random_event_today() if config['events']['use_events'] else ""
    style = get_random_greeting_style()
  
    
    other_people_text = additions['other_people_text'].format(num_other_people=num_people_in_channel)
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
        text = text_cleanup(text)

    
    except Exception as e:
        # if something goes wrong, just use a default message, kinda boring but better than nothing
        logger.error(f"Error generating chat completion: {e}")
        text = f"Hey {username}!"
    
    file_path = primary_tts.generate_speech(text)
    
    return file_path

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
    
    prompt_config = config['good_night_prompt']
    
    name = user.name
    styles = prompt_config['styles']
    
    
    sys_prompt = prompt_config['system']
    usr_prompt = prompt_config['user']
    sys_prompt = sys_prompt.format(language=language)
    usr_prompt = usr_prompt.format(name=name, style=random.choice(styles))
    
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": usr_prompt},
    ]
    
    text = primary_llm.generate_text(messages, max_tokens=1024)
    text = text_cleanup(text)
    logger.debug(f"generated greeting text: {text}")
    
    file = primary_tts.generate_speech(text)
    
    return file
    

def text_cleanup(text):
    text = remove_emoji.remove_emoji(text).replace('\"', '')
    return text