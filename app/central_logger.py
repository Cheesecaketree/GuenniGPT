import logging

# Get the discord.py logger
discord_logger = logging.getLogger("discord")

# Disable the discord.py logger
discord_logger.setLevel(logging.CRITICAL)

# Create a new formatter object
formatter = logging.Formatter('%(asctime)s %(levelname)s    %(name)s - %(message)s')

# Add the formatter object to a handler object
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler object to a logger object
logger = logging.getLogger('GuenniBot')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)