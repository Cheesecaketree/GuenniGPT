import discord
from discord.ext import commands
import logging
import asyncio
import datetime

import channel_queue
import background_utils as utils


logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', filename="logfile.log", level=logging.info)
logging.getLogger().addHandler(logging.StreamHandler())

description = utils.get_json("files/config.json")["description"]


bot = commands.Bot(command_prefix='?', description=description, intents=discord.Intents.default())

@bot.event
async def on_ready():
    time_str = datetime.datetime.now().strftime("%H:%M")
    print(f'it is {time_str}')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    logging.info(f"--- Bot ready at {time_str} ---")


# eventcontrolled functions
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    if member.voice is None: return
    # if is_muted(member): return # uses member to get voice channel
    
    # user joins voice channel
    if before.channel is not after.channel and after.channel is not None:
        # await asyncio.sleep(0.5)

        await voice_events("welcome", member)
        #await bot.change_presence(activity=discord.Game(random.choice(status))) # changes discord status of bot
        
    # # user deafens
    # elif after.self_deaf and not before.self_deaf:
    #     await voice_events("deaf", member)
        
    # # user starts stream
    # elif after.self_stream and not before.self_stream:
    #     await voice_events("stream", member)
    else: return
    

# starts eventcontrolled functions
async def voice_events(pEvent, member):
    username = str(member)
    channel = member.voice.channel
    channel_name = channel.name
    channel_lang = "de" # channel.guild.preferred_locale

    logging.info(f"Event {pEvent} triggered for {username}, language: {channel_lang}")
    
    file = None
    
    if pEvent == "welcome":
        file = utils.generate_greeting(name=username, channel=channel_name, language=channel_lang)
    else:
        return

    if file is not None:
        channel_queue.enqueue(file, channel_name)
        await queue_abspielen(member)
    else: 
        logging.error(f"File for {pEvent} could not be created")
    
    
    
    
# Verbindet mit einem Channel, wenn es möglich ist
async def create_connection(member):
    member_voice = member.voice.channel
    server = member.guild

    if server.voice_client is not None:
        return

    await member_voice.connect()
    logging.debug("Bot connected")


# Plays files from queue for channel of member
async def queue_abspielen(member):
    await create_connection(member)

    server = member.guild
    voice_connection = server.voice_client # Needs existing connection to work!
    
    channel_name = member.voice.channel.name
    queue_index = channel_queue.get_channel_pos(channel_name)

    while True:
        await create_connection(member)
        
        file = channel_queue.dequeue(queue_index)
        logging.info(f"{file} was removed from queue")
        
        logging.info(f"Now playing {file}")
        # with open(file, "rb") as f:
        voice_connection.play(discord.FFmpegPCMAudio(str(file)))
        
        while voice_connection.is_playing():
            await asyncio.sleep(0.1)
            
        await voice_connection.disconnect()
        voice_connection.cleanup() 
        channel_queue.queues[queue_index].done()
        utils.delete_file(file)

        if channel_queue.queues[queue_index].isEmpty():
            logging.debug("Queue is empty. Bot has disconnected.")
            return
        logging.debug("Queue not empty. Bot is playing next file")
    
    

# def is_muted(member):
#     events = utils.load_json("Files/events.json")
#     channel = member.voice.channel
#     channel_id = str(channel.id)
    
#     if channel_id in events["bot-mute"]:
#         mute_time = events["bot-mute"][channel_id]
#         if int(time.time()) > mute_time:
#             del events["bot-mute"][channel_id]
#             with open ("Files/events.json", "w") as f:
#                 json.dump(events, f)
#             return False
#         else:
#             return True
#     return False





token = utils.get_json("files/keys.json")["discord"]
bot.run(token)