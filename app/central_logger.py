import logging

# Create a new formatter object
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter object to a handler object
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler object to a logger object
logger = logging.getLogger('GuenniBot')
logger.addHandler(handler)