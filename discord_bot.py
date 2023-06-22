import discord
from discord.ext import commands
import logging
import asyncio
import datetime

import ai_requests as ai
import channel_queue
import background_utils as utils


logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', filename="logfile.log", level=logging.info)
logging.getLogger().addHandler(logging.StreamHandler())

description = utils.get_json("files/config.json")["description"]

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intent)


@bot.event
async def on_ready():
    time_str = datetime.datetime.now().strftime("%H:%M")
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
    

'''
Make sure the user is already in a voice channel before calling this function
'''
async def voice_events(pEvent, member, ctx=None):
    username = str(member)
    channel = member.voice.channel
    channel_name = channel.name
    channel_lang = "de" # channel.guild.preferred_locale

    logging.info(f"Event {pEvent} triggered for {username}, language: {channel_lang}")
    
    file = None
    
    if pEvent == "welcome":
        file = ai.generate_greeting(name=username, channel=channel_name, language=channel_lang)
    elif pEvent == "rating":
        file = ai.generate_rating(name=username, language=channel_lang)
        
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
        if member.voice is not None:
            voice_connection.play(discord.FFmpegPCMAudio(str(file)))
            
            while voice_connection.is_playing():
                await asyncio.sleep(0.1)
                
            await voice_connection.disconnect()
        voice_connection.cleanup() 
        utils.delete_file(str(file))
        channel_queue.queues[queue_index].done()
        

        if channel_queue.queues[queue_index].isEmpty():
            logging.debug("Queue is empty. Bot has disconnected.")
            return
        logging.debug("Queue not empty. Bot is playing next file")
    
    

@bot.command()
async def rateMe(ctx):
    if ctx.message.author.voice is None:
        logging.info("User tried to use rateMe command without being in a voice channel")
        await ctx.send("You need to be in a voice channel to use this command")
        return
    
    await voice_events("rating", ctx.message.author)





token = utils.get_json("files/keys.json")["discord"]
bot.run(token)