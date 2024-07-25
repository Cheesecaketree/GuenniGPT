import logging
from app_context import config

# Get the discord.py logger
discord_logger = logging.getLogger("discord")

# Disable the discord.py logger / set it to CRITICAL
discord_logger.setLevel(logging.CRITICAL)

# Create a new formatter object
formatter = logging.Formatter('%(asctime)s %(levelname)s    %(name)s - %(message)s')

# Add the formatter object to a handler object
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler object to a logger object
logger = logging.getLogger('GuenniBot')
logger.addHandler(handler)

# get logging level from config
if config["debug"] == True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

#logger.setLevel(logging.DEBUG)