import json
import tomllib

def load_config():
    with open('config/config.toml', mode="rb") as f:
        config = tomllib.load(f)
    return config

def load_keys():
    with open('config/keys.json') as f:
        keys = json.load(f)
    return keys

config = load_config()

keys = load_keys()