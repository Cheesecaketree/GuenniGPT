import openai
from background_utils import randStr
import remove_emoji
import datetime
from central_logger import logger
import voice_gen as voice
import random
import user_activity
from config import config, keys


    
openai.api_key = keys["openai"]
openai.organization = keys["openai-org"]


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
    filename = f"greeting_{randStr(N=4)}" + ".mp3"
    language = config["language"]
    
    username = str(user).split("#")[0] if not type(user) == str else user # if user is a string, it's already the username
    time_str = datetime.datetime.now().strftime("%H:%M")
    activity = user.activity if user.activity else None
    num_other_people = len(channel.members) - 1 
    # time_since_last_leave = user_activity.get_time_since_last_leave(channel.name, username) # in seconds
    
    # logger.debug(f"time since last leave: {time_since_last_leave}s")
    logger.debug(f"activity of {username}: {str(activity)}")
    logger.debug(f"number of other people in channel: {num_other_people}")
    
    event = get_random_event_today()
    style = get_random_greeting_style()
    logger.debug(f"chosen event: {event}")
    logger.debug(f"chosen greeting style: {style}")
    
    # weighted additions to the prompt
    additions = [
        {"weight": 1, "text": f"The channel is called {channel.name}."},
        {"weight": 2, "text": f"Today is {datetime.datetime.now().strftime('%A')}."},
        {"weight": 2, "text": f"It is currently {time_str}."},  
    ]

    #additions.append({"weight": 3, "text": f"They were last seen {round(time_since_last_leave/60)} minutes ago."}) if time_since_last_leave > 3600 else additions.append({"weight": 3, "text": f"They were last seen {round(time_since_last_leave / 3600)} hours ago."})
    additions.append({"weight": 3, "text": f"They are currently alone in the channel."}) if num_other_people == 0 else f"There are currently {num_other_people} other people in the channel."
    additions.append({"weight": 6, "text": f"{event}"}) if event else None
    additions.append({"weight": 4, "text": f"Their current activity is {activity}."}) if activity else None
    
    # choose a random addition based on the weights
    addition = random.choices(additions, weights=[entry["weight"] for entry in additions], k=1)[0]
    additions.remove(addition) # remove chosen addition from list so it doesn't get chosen for the second addition
    addition_text = addition["text"]
    logger.debug(f"addition text: {addition_text}")
    
    # choose a second addition but make sure it doesn"t repeat the first one and only do it occasionally
    if random.random() < 0.5:
        logger.debug("Second addition will be added")
        addition2 = random.choices(additions, weights=[entry["weight"] for entry in additions], k=1)[0]
        addition2_text = addition2["text"]
        logger.debug(f"second addition text: {addition2_text}")
        
        addition_text += addition2_text
        logger.debug(f"new addition text: {addition_text}")
    
    sys_message = f"Generate a {style} greeting for someone who just joined the Discord voice channel in at most three sentences. Only answer in {language} and keep it short."
    usr_message = f"User {username} joined a channel. {addition_text}"

    messages = [
        {"role": "system", "content": sys_message},
        {"role": "user", "content": usr_message},
    ]
    
    try:
        text = get_chatcompletion(messages, temperature=1, max_tokens=256)
        logger.debug(f"generated greeting text: {text}")
    except Exception as e:
        # if something goes wrong, just use a default message, kinda boring but better than nothing
        # not even sure if this can happen, but better safe than sorry
        logger.error(f"Error generating chat completion: {e}")
        text = f"Hey {username}!"
    
    voice.generate_audio(text, filename, language)
    
    return filename

# Returns a random greeting style from the config
def get_random_greeting_style():
    styles = config["greeting-styles"]
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

