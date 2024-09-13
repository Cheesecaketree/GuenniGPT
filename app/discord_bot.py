import discord
from discord.ext import commands

from central_logger import logger
import asyncio
import datetime

from app_context import config
import ai_requests as ai
import channel_queue
import background_utils as utils
import user_activity

import tempfile
import os


lang = config["language"]
description = config["description"]

intents = discord.Intents.all()

arg_length = config["max_arg_length"] if "max_arg_length" in config else 50 # max length of arguments in commands, 50 if not configured

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    #await bot.tree.sync() # sync command tree with discord
    logger.info(f"--- Bot ready at {datetime.datetime.now().strftime('%H:%M')} ---")
    
    
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
            file_path = ai.generate_greeting(user=member, channel=channel)
            try:
                await play_audio(file_path, member)
                
            except Exception as e:
                logger.error(f"Error playing audio file: {e}")
                
        return
    

# Command for syncing commands to guild
@bot.command(hidden=True)
@commands.guild_only()
@commands.is_owner()
async def sync_commands(ctx, guild_id: int = None):
    logger.debug("User used sync command")
    
    synced = await ctx.bot.tree.sync(guild=discord.Object(guild_id) if guild_id else None)
    
    
    logger.debug(f"Guild: {bot.get_guild(ctx.guild.id)}")
    
    await ctx.send(f"Synced commands {synced} to {bot.get_guild(ctx.guild.id) if guild_id else 'global'}")
    


@bot.tree.command(name="ping", description="Shows the latency of the bot")
async def ping(interaction: discord.Interaction):
    logger.debug("User used ping command")
    await interaction.response.send_message(f"Pong ({round(bot.latency * 1000)}ms)", ephemeral=True)


@bot.tree.command(name="rate", description="Rates a user. If name is not specified, rates you")
async def rate(interaction: discord.Interaction, name: str = None):
    logger.debug("User used rate command")
    user = interaction.user
    name = user.name if name is None else name
    
    # check if input is too long
    if len(name) > arg_length:
        logger.debug("User tried to use rate command with too long name")
        await interaction.response.send_message(f"Name too long. Max length is {arg_length} characters", ephemeral=True)
        return
    
    # check if user is in a voice channel
    if user.voice is None:
        logger.debug("User tried to use rating command without being in a voice channel")
        await interaction.response.send_message("You need to be in a voice channel to use this command", ephemeral=True)
        return
    
    
    await interaction.response.send_message(f"On my way to rate {name}!", ephemeral=True)
    
    logger.debug(f"Generating rating for {name}")
    file = ai.generate_rating(name=name)
     
    await play_audio(file, user)   


@bot.tree.command(name="compliment", description="Compliments a user. If name is not specified, compliments you")
async def compliment(interaction: discord.Interaction, name: str = None):
    logger.debug("User used compliment command")
    user = interaction.user
    name = user.name if name is None else name
    
    # check if input is too long
    if len(name) > arg_length:
        logger.debug("User tried to use compliment command with too long name")
        await interaction.response.send_message(f"Name too long. Max length is {arg_length} characters", ephemeral=True)
        return
    
    # check if user is in a voice channel
    if user.voice is None:
        logger.debug("User tried to use compliment command without being in a voice channel")
        await interaction.response.send_message("You need to be in a voice channel to use this command", ephemeral=True)
        return
    
    await interaction.response.send_message(f"On my way to compliment {name}!", ephemeral=True)
    
    logger.debug(f"Generating compliment for {name}")
    file = ai.generate_compliment(name=name)
    
    await play_audio(file, user)   


@bot.tree.command(name="hello", description="Say hello to someone")
async def hello(interaction: discord.Interaction, name: str = None):
    logger.debug("User used hello command")
    user = interaction.user
    if name is None:
        logger.debug("User did not specify name")
        await interaction.response.send_message("You need to specify a name", ephemeral=True)
        return
    
    # check if input is too long
    if len(name) > arg_length:
        logger.debug("User tried to use hello command with too long name")
        await interaction.response.send_message(f"Name too long. Max length is {arg_length} characters", ephemeral=True)
        return
    
    # check if user is in a voice channel
    if user.voice is None:
        logger.debug("User tried to use hello command without being in a voice channel")
        await interaction.response.send_message("You need to be in a voice channel to use this command", ephemeral=True)
        return
    
    await interaction.response.send_message(f"On my way to say hello to {name}!", ephemeral=True)
    
    file = ai.generate_greeting(name, user.voice.channel)

    await play_audio(file, user)

@bot.tree.command(name="good_night", description="Wishes a user good night.")
async def good_night(interaction: discord.Interaction, name: str = None):
    logger.debug("User used good night command")
    user = interaction.user
    name = user.name if name is None else name
    
    # check if input is too long
    if len(name) > arg_length:
        logger.debug("User tried to use good night command with too long name")
        await interaction.response.send_message(f"Name too long. Max length is {arg_length} characters", ephemeral=True)
        return
    
    # check if user is in a voice channel
    if user.voice is None:
        logger.debug("User tried to use good night command without being in a voice channel")
        await interaction.response.send_message("You need to be in a voice channel to use this command", ephemeral=True)
        return
    
    await interaction.response.send_message(f"Good night {name}!", ephemeral=True)
    
    file = ai.generate_good_night(user)

    await play_audio(file, user)




# connects bot to voice channel of member
async def create_connection(member):
    logger.debug(f"Creating connection to voice channel for user {member.name}")
    member_voice = member.voice.channel
    server = member.guild

    if server.voice_client is not None:
        return

    await member_voice.connect()
    logger.debug("Bot connected to voice")

    
# enqueues the file and plays it 
# file is a byte stream object
async def play_audio(file_path, member):
    channel_queue.enqueue(file_path, channel_name=member.voice.channel.name)
    
    await create_connection(member)

    server = member.guild
    voice_connection = server.voice_client
    
    channel_name = member.voice.channel.name
    queue_index = channel_queue.get_channel_pos(channel_name)


    await create_connection(member)
    queue_file_path = channel_queue.dequeue(queue_index)
    
    if member.voice is not None:

        ffmpeg_audio = discord.FFmpegPCMAudio(queue_file_path)
        
            
        voice_connection.play(ffmpeg_audio)
        
        while voice_connection.is_playing():
            await asyncio.sleep(1)
        
        if not channel_queue.queues[queue_index].isEmpty():
                next_file = channel_queue.dequeue(queue_index)
                asyncio.create_task(play_audio(next_file, member))
                return
        
        await voice_connection.disconnect()
        voice_connection.cleanup()
        os.remove(queue_file_path)
        channel_queue.queues[queue_index].done()
        
            
        
token = config['keys']['discord']
bot.run(token)