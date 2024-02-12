from central_logger import logger
import time
from config import config

user_last_leave = {}

# check if user was already in channel in the last few minutes (timeout)

def get_user_recently_left(channel, member):
    # get timeout from config.json
    timeout = config['timeout']
    
    if channel not in user_last_leave or member not in user_last_leave[channel] or user_last_leave[channel][member] + timeout < time.time():
        return False
    
    return True

def set_user_recently_left(channel, member):
    logger.info(f"set_user_recently_left: {channel} {member} {time.time()}")
    if channel not in user_last_leave:
        user_last_leave[channel] = {}
    user_last_leave[channel][member] = time.time()
    return
    
def get_time_since_last_leave(channel, member):
    if channel not in user_last_leave or member not in user_last_leave[channel]:
        return 0
    return time.time() - user_last_leave[channel][member]