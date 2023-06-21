import openai
import json
import os

openai.organization = "org-UmjtjEZDwQcO8rvQHs8tiGKZ"
openai.api_key_path = os.path.expanduser("./key")

def greet(name, channel):
    language = "de"
    time_str = "12:00am"
    
    system_msg = system_message = {
        "role": "system", "content": "You are a discord bot that greets people joining a voice channel. You get passed name, channel, time and server language. Greet them in a funny and creative way. Keep it short, use the given language, dont use emojis."
    }
    
    messages = [
        system_message,
        {"role": "user", "content": f"lang={de}, {name} joined channel \"{channel.name}\" at {time_str}"},
    ]
    
    response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = messages,
    ) 

    response_message = response.choices[0].message.content
    
    return response_message