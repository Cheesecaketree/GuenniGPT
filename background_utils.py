import json
import random
import string
import logging
import os
import tiktoken



def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens_integer = encoding.encode(text)
    number_of_tokens = len(tokens_integer)
    return number_of_tokens
    

def get_json(path):
    with open(path, "r") as f:
        return json.load(f)


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