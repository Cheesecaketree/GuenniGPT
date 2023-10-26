import discord
from discord.ext import commands
import logging
import asyncio
import datetime

from config import config
import ai_requests as ai
import channel_queue
import background_utils as utils
import user_activity

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s| %(message)s', level=logging.WARN)
logging.getLogger().addHandler(logging.StreamHandler())

# deactivate logging for discord
logging.getLogger('discord.client').setLevel(logging.WARN)
logging.getLogger('discord.gateway').setLevel(logging.WARN)
logging.getLogger('discord.voice_client').setLevel(logging.WARN)

lang = config["language"] # utils.get_json("config/config.json")["language"]
description = config["description"] # utils.get_json("config/config.json")["description"]

intent = discord.Intents.default()
intent = discord.Intents(guilds=True, members=True, presences=True, voice_states=True)
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
    #if member.voice is None: return
    
    file = None
    
    username = str(member)
    
    # user leaves voice channel
    if before.channel is not None and after.channel is not before.channel: 
        logging.debug(f"{username} left {before.channel.name}")
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
            logging.info(f"{username} recently joined {channel_name}")
        else:
            # generates audio and plays it
            file = ai.generate_greeting(user=member, channel=channel, pLanguage=channel_lang)
            try:
                await play_audio(file, member)
            except Exception as e:
                logging.error(f"Error playing audio file: {e}")
                utils.delete_file(str(file))
        return
    

@bot.command()
async def rating(ctx, name=None):
    user = ctx.message.author
    if name is None:
        name = user.name
        
    if user.voice is None:
        logging.debug("User tried to use rating command without being in a voice channel")
        await ctx.send("You need to be in a voice channel to use this command")
        return
    
    file = ai.generate_rating(name=name, pLanguage=lang)
        
    await play_audio(file, user)   


@bot.command()
async def compliment(ctx, name=None):
    user = ctx.message.author
    if name is None:
        name = user.name
        
    if user.voice is None:
        logging.debug("User tried to use compliment command without being in a voice channel")
        await ctx.send("You need to be in a voice channel to use this command")
        return
    
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
    member_voice = member.voice.channel
    server = member.guild

    if server.voice_client is not None:
        return

    await member_voice.connect()
    logging.debug("Bot connected to voice")

    
# enqueues the file and plays it 
async def play_audio(file, member):
    channel_queue.enqueue(file, channel_name=member.voice.channel.name)
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
        


token = utils.get_json("config/keys.json")["discord"]
bot.run(token)