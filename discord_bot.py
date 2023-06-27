import discord
from discord.ext import commands
import logging
import asyncio
import datetime

import ai_requests as ai
import channel_queue
import background_utils as utils


logging.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s| %(message)s', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

# deactivate logging for discord
logging.getLogger('discord.client').setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.WARN)

lang = utils.get_json("files/config.json")["language"]
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
    
    file = None
    
    username = str(member)
    channel = member.voice.channel
    channel_name = channel.name
    channel_lang = lang
    activity = member.activity
    
    # user joins voice channel
    if before.channel is not after.channel and after.channel is not None:
        file = ai.generate_greeting(name=username, channel=channel_name, pLanguage=channel_lang, activity=activity)
        await play_audio(file, member)
        return
                
    else: return
    

@bot.command()
async def rating(ctx, name=None):
    user = ctx.message.author
    if name is None:
        name = user.name
        
    if user.voice is None:
        logging.debug("User tried to use rateMe command without being in a voice channel")
        await ctx.send("You need to be in a voice channel to use this command")
        return
    
    file = ai.generate_rating(name=name, pLanguage=lang)
        
    await play_audio(file, user)   


@bot.command()
async def talkAbout(ctx, topic):
    user = ctx.message.author
    if user.voice is None:
        await ctx.send("You need to be in a voice channel to use this command")
        return
    
    if topic is None:
        await ctx.send("Please specify a topic")
        return
    
    file = ai.generate_talk_about(topic=topic, pLanguage=lang)
    
    await play_audio(file, user)
    
    
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
        


token = utils.get_json("files/keys.json")["discord"]
bot.run(token)