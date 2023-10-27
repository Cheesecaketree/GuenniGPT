from central_logger import logger
from audio_queue import AudioQueue


queues = []

def get_channel_pos(channel_name):
    for queue in queues:
        if queue.get_name() == channel_name:
            return queues.index(queue)

def enqueue(filename, channel_name):
    if channel_name not in [queue.get_name() for queue in queues]:
        logger.debug(f"channel queue created. ID: {channel_name}")
        queues.append(AudioQueue(channel_name))

    try:
        queues[get_channel_pos(channel_name)].enqueue(filename)
        logger.debug(f"{filename} added to channel queue {channel_name}")
    except:
        logger.critical("filename could not be added to channel queue! enqueue()")
    

def dequeue(queue_index):
    try:
        return queues[queue_index].dequeue()
    except:
        logger.critical(f"Could not dequeue from {queues[queue_index].get_name()}! In channel_queue_dequeue()")
