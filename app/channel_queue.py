import logging
from audio_queue import AudioQueue

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',filename='logfile.log', level=logging.INFO)


queues = []

def get_channel_pos(channel_name):
    for queue in queues:
        if queue.get_name() == channel_name:
            return queues.index(queue)

def enqueue(filename, channel_name):
    if channel_name not in [queue.get_name() for queue in queues]:
        logging.debug(f"channel queue created. ID: {channel_name}")
        queues.append(AudioQueue(channel_name))

    try:
        queues[get_channel_pos(channel_name)].enqueue(filename)
        logging.debug(f"{filename} added to channel queue {channel_name}")
    except:
        logging.critical("filename could not be added to channel queue! enqueue()")
    

def dequeue(queue_index):
    try:
        return queues[queue_index].dequeue()
    except:
        logging.critical(f"Could not dequeue from {queues[queue_index].get_name()}! In channel_queue_dequeue()")
