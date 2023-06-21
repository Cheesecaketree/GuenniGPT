import openai
import background_utils as utils
import remove_emoji
import json
import datetime
import logging



with open("files/keys.json", "r") as f:
    out = json.load(f)
    
openai.api_key = out["openai"]
openai.organization = out["openai-org"]

total_tokens = 0

def greet(name, channel, language):
    time_str = datetime.datetime.now().strftime("%H:%M")
    logging.info(f"Time: {time_str}")
    
    #"role": "system", "content": "You are a discord bot that greets people joining a voice chat. You get passed the name of the person, the channel they are joining, the time and the server language. Greet them in a funny and creative way. Keep it short, be rude, always use the given language"
    system_msg = {
        "role": "system", "content": "You are a discord bot that greets people joining a voice chat. You get passed the name of the person, the time and the server language. Greet them in a funny and creative way. Keep it short, be rude, always use the given language"
    }
    
    messages = [
        system_msg,
        {"role": "user", "content": f"lang={language}, {name} joined channel \"{channel}\" at {time_str}"},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=256,
    )


    response_message = response.choices[0].message.content
    
    # strip the response from emojis, special characters and newlines
    
    
    
    response_message = remove_emoji.remove_emoji(response_message)
    
    return response_message