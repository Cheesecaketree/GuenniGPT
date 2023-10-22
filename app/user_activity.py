import logging
import time

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',filename='logfile.log', level=logging.INFO)


user_last_leave = {}

# check if user was already in channel in the last few minutes (timeout)
import json

def get_user_recently_left(channel, member):
    # get timeout from config.json
    with open('config/config.json') as f:
        config = json.load(f)
    timeout = config['timeout']
    
    
    if channel not in user_last_leave or member not in user_last_leave[channel] or user_last_leave[channel][member] + timeout < time.time():
        return False
    
    return True

def set_user_recently_left(channel, member):
    logging.info(f"set_user_recently_left: {channel} {member} {time.time()}")
    if channel not in user_last_leave:
        user_last_leave[channel] = {}
    user_last_leave[channel][member] = time.time()
    return
    