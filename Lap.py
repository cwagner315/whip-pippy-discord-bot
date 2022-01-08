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

intents = discord.Intents.default()
intents.members = True

targetMember = None
acussingMember = None
voteIds = []
voteActive = False
voteChannel = None
voteUserId = ''
voteStartTime = datetime.now()
votesRequired = 0

muteActive = False
muteTime = 0
muteStartTime = datetime.now()

bot = Bot("!")

@tasks.loop(seconds = 1) # repeat after every 1 seconds
async def countdownLoop():
    global voteIds, voteActive, voteStartTime, voteChannel, voteUserId, muteActive, muteStartTime, muteTime
    
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    channel = voteChannel
        
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
            await channel.send(f'Votes now closed. Better luck next time fuck nugget @{acussingMember.name}!')

    muteTimeDelta = (datetime.now() - muteStartTime)
    muteTimeDelta = math.floor(muteTimeDelta.total_seconds())

    if muteActive:
        if muteTimeDelta == muteTime:
            await channel.send(f'The {muteTime} second mute has been lifted! @{targetMember.name}')
            muteActive = False
            muteTime = 0
            await set_to_unmuted(targetMember)


@bot.command(intents = intents, help = 'Intiates a one minute vote for (3/5) of the target members current voice channel non-self-defeaned members to cast a vote by typing !lap\rif the mute is successful it will server mute the target user for a random amount of seconds between 15-120.\nCommand use: !lap Optional[target] to start a vote.\r\rex: \r\t!lap @pipe_down\r\t!lap # Defaults: @pipe_down\r')
async def lap(ctx, target : Optional[discord.Member] = None):
    global voteIds, voteActive, voteChannel, voteStartTime, votesRequired, muteStartTime, muteTime, muteActive, targetMember, acussingMember
    
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
            response = f'You can\'t vote twice fuck face! Yes.. I am talking to you @{ctx.author.name}'
        else:
            voteIds.insert(len(voteIds), ctx.author.id)

            if len(voteIds) == 1:
                if target.voice:
                    channel = target.voice.channel
                    voiceMembers = channel.members
                    print(f"Total Members: {len(voiceMembers)}")
                    votesRequired = 0
                    for member in voiceMembers:
                        print(f"Member: {member.name}")
                        if not member.voice.self_deaf:
                            votesRequired = votesRequired + 1
                            print(f"Added Vote: {votesRequired}")
                    
                    if votesRequired > 0:
                        votesRequired = math.floor(votesRequired * (3/5))

                print(f"Pre-Votes Required: {votesRequired}")
                if not (votesRequired >= 3):
                    votesRequired = 3
                
                print(f"Final Votes Required: {votesRequired}")
                response = f'@{ctx.author.name} has intiated a vote to mute @{target.name}! "!lap" to vote ({len(voteIds)} / {votesRequired})'
                voteActive = True
                voteStartTime = datetime.now()
                voteChannel = ctx.channel
            elif len(voteIds) >= votesRequired:
                muteTime = random.randint(15, 120)
                muteStartTime = datetime.now()
                muteActive = True
                response = f'@{ctx.author.name} put the final nail in the coffin! ({len(voteIds)} / {votesRequired})\n@{target.name} will be muted for {muteTime} seconds!'
                voteIds = []
                voteActive = False
                await set_to_muted(target)
            else:
                response = f'@{ctx.author.name} has spoken! ({len(voteIds)} / {votesRequired})'
        await ctx.send(response)
    else:
        await ctx.send(f"I am currently muting @{targetMember.name}.. like tf chill out and get the fuck outta my face @{ctx.author.name} dumb ass bitch!")

async def set_to_muted(member: discord.Member):
    await member.edit(mute=True)

async def set_to_unmuted(member: discord.Member):
    await member.edit(mute=False)

countdownLoop.start()  
bot.run(TOKEN)