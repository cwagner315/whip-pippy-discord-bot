# TakeALap.py
# executable="C:/ffmpeg/bin/ffmpeg.exe", <-- for winows machines..
import os

import math
import random
from dotenv import load_dotenv
from typing import Optional
import discord
from discord.ext import tasks
from discord.ext.commands import Bot
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PIPEDOWN = os.getenv('DISCORD_PIPE_DOWN_ID')

targetMember = None
acussingMember = None
voteIds = []
voteActive = False
voteChannelId = ''
voteUserId = ''
voteStartTime = datetime.now()

muteActive = False
muteTime = 0
muteStartTime = datetime.now()

bot = Bot("!")

@tasks.loop(seconds = 1) # repeat after every 1 seconds
async def countdownLoop():
    global voteIds, voteActive, voteStartTime, voteChannelId, voteUserId, muteActive, muteStartTime, muteTime
    
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    channel = bot.get_channel(id=voteChannelId)
        
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
            await channel.send(f'Votes now closed. Better luck next time fuck nugget {acussingMember.mention}!')

    muteTimeDelta = (datetime.now() - muteStartTime)
    muteTimeDelta = math.floor(muteTimeDelta.total_seconds())

    if muteActive:
        if muteTimeDelta == muteTime:
            await channel.send(f'The {muteTime} second mute has been lifted! {targetMember.mention}')
            muteActive = False
            muteTime = 0
            await set_to_unmuted(targetMember)


@bot.command()
async def lap(ctx, target : Optional[discord.Member] = None):
    global voteIds, voteActive, voteChannelId, voteStartTime, muteStartTime, muteTime, muteActive, targetMember, acussingMember
    
    if not muteActive:
        if not voteActive:
            if not target:    
                global PIPEDOWN
                pipedown = await ctx.guild.query_members(user_ids=[PIPEDOWN])
                target = pipedown[0]
            targetMember = target
            acussingMember = ctx.author
        else:
            target = targetMember

        if ctx.author.id in voteIds:
            response = f'You can\'t vote twice fuck face! Yes.. I am talking to you {ctx.author.mention}'
        else:
            voteIds.insert(len(voteIds), ctx.author.id)

            if len(voteIds) == 1:
                response = f'{ctx.author.mention} has intiated a vote to mute {target.mention}! "!lap" to vote ({len(voteIds)} / 5)'
                voteActive = True
                voteStartTime = datetime.now()
                voteChannelId = ctx.channel.id 
            elif len(voteIds) == 2:
                muteTime = random.randint(15, 120)
                muteStartTime = datetime.now()
                muteActive = True
                response = f'{ctx.author.mention} put the final nail in the coffin! ({len(voteIds)} / 5)\n{target.mention} will be muted for {muteTime} seconds!'
                voteIds = []
                voteActive = False
                await set_to_muted(target)
            else:
                response = f'{ctx.author.mention} has spoken! ({len(voteIds)} / 5)'
        await ctx.send(response)
    else:
        await ctx.send(f"I am currently muting {targetMember.mention}.. like tf chill out and get the fuck outta my face {ctx.author.mention} dumb ass bitch!")

async def set_to_muted(member: discord.Member):
    await member.edit(mute=True)

async def set_to_unmuted(member: discord.Member):
    await member.edit(mute=False)

countdownLoop.start()  
bot.run(TOKEN)