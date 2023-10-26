import json

def load_config():
    with open('config/config.json') as f:
        config = json.load(f)
    return config

config = load_config()