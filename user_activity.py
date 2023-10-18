import logging
import time

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',filename='logfile.log', level=logging.INFO)


user_last_join = {}

# check if user was already in channel in the last minute
def user_recently_joined(channel, member):
    
    if channel not in user_last_join or member not in user_last_join[channel] or user_last_join[channel][member] + 600 < time.time():
        user_last_join[channel] = {}
        user_last_join[channel][member] = time.time()
        return False
    
    user_last_join[channel] = {}
    user_last_join[channel][member] = time.time()
    return True
    