# Lap.py
import os

import math
import random
import asyncio
import discord
from discord.ext import tasks
from datetime import date, datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PIPEDOWN = os.getenv('DISCORD_PIPE_DOWN_ID')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

voteIds = []
voteActive = False
voteChannelId = ''
voteUserId = ''
voteStartTime = datetime.now()

muteActive = False
muteTime = 0
muteStartTime = datetime.now()

@tasks.loop(seconds = 1) # repeat after every 1 seconds
async def countdownLoop():
    global voteIds, voteActive, voteStartTime, voteChannelId, voteUserId, muteActive, muteStartTime, muteTime
    
    await client.wait_until_ready()
    
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    pipedown = await guild.query_members(user_ids=[PIPEDOWN])
    pipedown = pipedown[0]

    channel = client.get_channel(id=voteChannelId)
        
    timeDelta = (datetime.now() - voteStartTime)
    timeDelta = math.floor(timeDelta.total_seconds())

    if voteActive:
        if timeDelta == 2:
            await channel.send(f'One Minute Remaining...')
        elif timeDelta == 32:
            await channel.send(f'Thirty Seconds Remaining...')
        elif timeDelta == 62:
            voteActive = False
            voteIds = []
            await channel.send(f'Votes now closed. Better luck next time fuck nugget !')

    muteTimeDelta = (datetime.now() - muteStartTime)
    muteTimeDelta = math.floor(muteTimeDelta.total_seconds())

    if muteActive:
        if muteTimeDelta == muteTime:
            await channel.send(f'The {muteTime} second mute has been lifted! {pipedown.mention}')
            muteActive = False
            muteTime = 0
            await set_to_unmuted(pipedown)

@client.event
async def on_message(message):
    global voteIds, voteActive, voteChannelId, voteStartTime, muteStartTime, muteTime, muteActive
    global PIPEDOWN
    pipedown = await message.guild.query_members(user_ids=[PIPEDOWN])
    pipedown = pipedown[0]
    
    if message.author == client.user:
        return

    if message.content == '!lap':
        if message.author.id in voteIds:
            response = f'You can\'t vote twice fuck face! Yes.. I am talking to you {message.author.mention}'
        else:
            voteIds.insert(len(voteIds), message.author.id)

            if len(voteIds) == 1:
                response = f'{message.author.mention} has intiated a vote to mute {pipedown.mention}! "!lap" to vote ({len(voteIds)} / 5)'
                voteActive = True
                voteStartTime = datetime.now()
                voteChannelId = message.channel.id 
            elif len(voteIds) == 5:
                muteTime = random.randint(15, 60)
                muteStartTime = datetime.now()
                muteActive = True
                response = f'{message.author.mention} put the final nail in the coffin! ({len(voteIds)} / 5)\n{pipedown.mention} will be muted for {muteTime} seconds!'
                voteIds = []
                voteActive = False
                await set_to_muted(pipedown)
            else:
                response = f'{message.author.mention} has spoken! ({len(voteIds)} / 5)'
        await message.channel.send(response)

async def set_to_muted(member: discord.Member):
    await member.edit(mute=True)

async def set_to_unmuted(member: discord.Member):
    await member.edit(mute=False)

countdownLoop.start()     
client.run(TOKEN)