import discord

from discord.ext import commands
from central_logger import logger
import asyncio
import datetime

from config import config, keys
import ai_requests as ai
import channel_queue
import background_utils as utils
import user_activity


lang = config["language"] # utils.get_json("config/config.json")["language"]
description = config["description"] # utils.get_json("config/config.json")["description"]

intents = discord.Intents.default()
intents = discord.Intents(guilds=True, members=True, presences=True, voice_states=True)
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    time_str = datetime.datetime.now().strftime("%H:%M")
    logger.info(f"--- Bot ready at {time_str} ---")
    
    



# eventcontrolled functions
@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    #if member.voice is None: return
    
    file = None
    
    username = str(member)
    
    # user leaves voice channel
    if before.channel is not None and after.channel is not before.channel: 
        logger.debug(f"{username} left {before.channel.name}")
        # set user_last_leave to current time
        user_activity.set_user_recently_left(before.channel.name, username)
        return
    
    # user joins voice channel
    if before.channel is not after.channel and after.channel is not None:
        channel = member.voice.channel
        channel_name = channel.name
        channel_lang = lang
        
        # check if user was already in channel in the last 10 minutes
        if user_activity.get_user_recently_left(channel_name, username):
            logger.info(f"{username} recently joined {channel_name}")
        else:
            # generates audio and plays it
            file = ai.generate_greeting(user=member, channel=channel, pLanguage=channel_lang)
            try:
                await play_audio(file, member)
            except Exception as e:
                logger.error(f"Error playing audio file: {e}")
                utils.delete_file(str(file))
        return
    


@bot.command(name = "ping", description = "ping command") # TODO: remove guild  , guild=discord.Object(id=603978404198612993)
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def rating(ctx, name=None):
    user = ctx.message.author
    if name is None:
        name = user.name
        
    if user.voice is None:
        logger.debug("User tried to use rating command without being in a voice channel")
        await ctx.send("You need to be in a voice channel to use this command")
        return
    
    logger.debug(f"Generating rating for {name}")
    file = ai.generate_rating(name=name, pLanguage=lang)
        
    await play_audio(file, user)   


@bot.command()
async def compliment(ctx, name=None):
    user = ctx.message.author
    if name is None:
        name = user.name
        
    if user.voice is None:
        logger.debug("User tried to use compliment command without being in a voice channel")
        await ctx.send("You need to be in a voice channel to use this command")
        return
    
    logger.debug(f"Generating compliment for {name}")
    file = ai.generate_compliment(name=name, pLanguage=lang)
        
    await play_audio(file, user)   


# @bot.command()
# async def talkAbout(ctx, topic=None):
#     user = ctx.message.author
#     if user.voice is None:
#         await ctx.send("You need to be in a voice channel to use this command")
#         return
    
#     if topic is None:
#         await ctx.send("Please specify a topic")
#         return
    
#     file = ai.generate_talk_about(topic=topic, pLanguage=lang)
    
#     await play_audio(file, user)
    


# connects bot to voice channel of member
async def create_connection(member):
    logger.debug("Creating connection to voice channel for user {member.name}")
    member_voice = member.voice.channel
    server = member.guild

    if server.voice_client is not None:
        return

    await member_voice.connect()
    logger.debug("Bot connected to voice")

    
# enqueues the file and plays it 
async def play_audio(file, member):
    channel_queue.enqueue(file, channel_name=member.voice.channel.name)
    logger.debug(f"Enqueued file {file} for {member.name}")
    await create_connection(member)

    server = member.guild
    voice_connection = server.voice_client
    
    channel_name = member.voice.channel.name
    queue_index = channel_queue.get_channel_pos(channel_name)

    while True:
        await create_connection(member)
        file = channel_queue.dequeue(queue_index)
        
        # with open(file, "rb") as f:
        if member.voice is not None:
            logger.info(f"Now playing file: {file}")
            voice_connection.play(discord.FFmpegPCMAudio(str(file)))
            
            while voice_connection.is_playing():
                await asyncio.sleep(0.1)
                
            await voice_connection.disconnect()
        voice_connection.cleanup() 
        utils.delete_file(str(file))
        channel_queue.queues[queue_index].done()
        

        if channel_queue.queues[queue_index].isEmpty():
            logger.debug("Queue is empty. Bot has disconnected.")
            return
        logger.debug("Queue not empty. Bot is playing next file")
        


token = keys["discord"]
bot.run(token)