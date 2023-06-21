import json
import random
import string
import logging
import os
import tiktoken

from gtts import gTTS
import ai_requests


logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', filename="logfile.log", level=logging.INFO)

def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens_integer = encoding.encode(text)
    number_of_tokens = len(tokens_integer)
    

def get_json(path):
    with open(path, "r") as f:
        return json.load(f)
    
    
def generate_greeting(name, channel, language):
    name = name.split("#")[0]
    filename = f"greeting_{randStr(N=4)}" + ".mp3"
    text = ai_requests.greet(name, channel, language)
    
    logging.info(f"Generating greeting for {name} in {channel} with language {language} \n Text: {text}")
    
    generate_voice(text, filename, language)
    
    return filename
    
    
def generate_voice(pText, filename, language): 
    logging.info(f"Generating voice in lang {language}, Text: {pText}")
    nachricht = gTTS(text=pText, lang=language)
    filename = filename
    nachricht.save(filename)
    logging.info(f"{filename} created")




def delete_file(file):
    os.remove(file)
    
def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string