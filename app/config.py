import json

def load_config():
    with open('config/config.json') as f:
        config = json.load(f)
    return config

def load_keys():
    with open('config/keys.json') as f:
        keys = json.load(f)
    return keys

config = load_config()

keys = load_keys()