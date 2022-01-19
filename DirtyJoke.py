# DirtyJoke.py
# executable="C:/ffmpeg/bin/ffmpeg.exe", <-- for winows machines..
import os
import time
import random
import discord
import pyttsx3
from gtts import gTTS
import asyncio
from dotenv import load_dotenv
from discord.ext.commands import Bot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

jokeList = [
	('What did the toaster say to the slice of bread? "I want you inside me."'), 
	('"Give it to me! Give it to me!" she yelled. "I\'m so wet, give it to me now!" She could scream all she wanted, but I was keeping the umbrella.'), 
	('Two men broke into a drugstore and stole all the Viagra. The police put out an alert to be on the lookout for the two hardened criminals.'), 
	('They say that during sex you burn off as many calories as running eight miles. Who the hell runs eight miles in 30 seconds?'), 
	('I\'ll admit it, I have a tremendous sex drive. My girlfriend lives forty miles away.'), 
	('Who\'s the most popular guy at the nudist colony? The one who can carry a cup of coffee in each hand and a dozen doughnuts.'), 
	('What\'s the difference between kinky and perverted? Kinky is when you tickle your girlfriend with a feather, perverted is when you use the whole bird.'), 
	('"I bet you can\'t tell me something that will make me both happy and sad at the same time," a husband says to his wife. She thinks about it for a moment and then responds, "Your penis is bigger than your brother\'s."'), 
	('A woman walks out of the shower, winks at her boyfriend, and says, "Honey, I shaved myself down there. Do you know what that means?" The boyfriend says, "Yeah, it means the drain is clogged again."'), 
	('How do you make a pool table laugh? Tickle its balls.'), 
	('If you were born in September, it\'s pretty safe to assume that your parents started their new year with a bang.'), 
	('A naked man broke into a church. The police chased him around and finally caught him by the organ.'), 
	('Did you hear about the constipated accountant? He couldn\'t budget, so he had to work it out with a paper and pencil.'), 
	('Why did the sperm cross the road? Because I put on the wrong sock this morning.'), 
	('An old woman walked into a dentist\'s office, took off all her clothes, and spread her legs. The dentist said, "I think you have the wrong room." "You put in my husband\'s teeth last week," she replied. "Now you have to remove them."'), 
	('Why does a mermaid wear seashells? Because she outgrew her B-shells!'), 
	('What do you call a cheap circumcision? A rip-off!'), 
	('What do you do when your cat\'s dead? Play with the neighbor\'s pussy instead.'), 
	('How is life like toilet paper? You\'re either on a roll or taking shit from someone.'), 
	('What\'s the difference between a tire and 365 used condoms? One\'s a Goodyear. The other\'s a great year.'), 
	('What is Moby Dick\'s dad\'s name? Papa Boner.'), 
	('What do you call someone who refuses to fart in public? A private tutor!'), 
	('What do you call a herd of cows masturbating? Beef strokin\' off!'), 
	('What did the leper say to the sex worker? Keep the tip.'), 
	('What do you call the lesbian version of a cock block? A beaver dam!'), 
	('What do a penis and a Rubik\'s Cube have in common? The more you play with it, the harder it gets.'), 
	('What\'s long, green, and smells like bacon? Kermit The Frog\'s fingers!'), 
	('What do you get when you jingle Santa\'s balls? A white Christmas!'), 
	('Why is diarrhea hereditary? It runs in your genes!'), 
	('A penguin takes his car to the shop and the mechanic says it\'ll take about an hour for him to check it. While he waits, the penguin goes to an ice cream shop and orders a big sundae to pass the time. The penguin isn\'t the neatest eater, and he ends up covered in melted ice cream. When he returns to the shop, the mechanic takes one look at him and says, "Looks like you blew a seal." "No," the penguin insists, "it\'s just ice cream."'), 
	('What did one butt cheek say to the other? Together, we can stop this crap.'), 
	('A man and a woman started to have sex in the middle of a dark forest. After about 15 minutes, the man finally gets up and says, "Damn, I wish I had a flashlight!" The woman says, "Me too, you\'ve been eating grass for the past ten minutes!"'), 
	('What do you get when you cross a dick with a potato? A dictator!'), 
	('How is sex like a game of bridge? If you have a great hand, you don\'t need a partner.'), 
	('My neighbor has been mad at his wife for sunbathing nude. I personally am on the fence.'), 
	('What do you call an expert fisherman? A Master Baiter.'), 
	('How can you tell if your husband is dead? The sex is the same, but you get to use the remote.'), 
	('"I\'d rather go through the pain of childbirth again than let you drill in my mouth," the woman told her dentist. He replied, "Well, please make up your mind so I can adjust my chair."'), 
	('Why did the squirrel swim on its back? To keep its nuts dry.'), 
	('What\'s the difference between a genealogist and a gynecologist? A genealogist looks up the family tree, a gynecologist looks up the family bush.'), 
	('Why can\'t you hear rabbits making love? Because they have cotton balls.'), 
	('If your Uncle Jack was on his roof, and he wanted you to help him down, would you help your Uncle Jack off?'), 
	('What comes after 69? Mouthwash.'), 
	('What does Pinocchio\'s lover say to him? "Lie to me! Lie to me!"'), 
	('Dear NASA: Your mom thought I was big enough.–Pluto'), 
	('What\'s the difference between a pickpocket and a peeping tom? One snatches your watch. The other watches your snatch.'), 
	('A guy is sitting at the doctor\'s office. The doctor walks in and says, "I have some bad news. I\'m afraid you\'re going to have to stop masturbating." "I don\'t understand, doc," the patient says. "Why?" "Because," the doctor says. "I\'m trying to examine you."'), 
	('What do a nearsighted gynecologist and a puppy have in common? A wet nose.'), 
	('How do you make your girlfriend scream during sex? Call and tell her about it.'), 
	('Why does Dr. Pepper come in a bottle? Because his wife died!'), 
	('What\'s the difference between hungry and horny? Where you stick the cucumber.'), 
	('Why isn\'t there a pregnant Barbie doll? Ken came in another box.'), 
	('What goes in hard and dry, but comes out soft and wet? Gum!'), 
	('What\'s the process of applying for a job at Hooters? They just give you a bra and say, "Here, fill this out."'), 
	('What are the three shortest words in the English language? "Is it in?"'), 
	('How does a woman scare a gynecologist? By becoming a ventriloquist.'), 
	('What\'s the difference between your penis and a bonus check? Someone\'s always willing to blow your bonus.'), 
	('What\'s the difference between an oral and a rectal thermometer? The taste!'), 
	('What does the sign on an out-of-business brothel say? Beat it. We\'re closed.'), 
	('A family\'s driving behind a garbage truck when a dildo flies out and thumps against the windshield. Embarrassed, and trying to spare her young son\'s innocence, the mother turns around and says, "Don\'t worry, dear. That was just an insect." "Wow," the boy replies. "I\'m surprised it could get off the ground with a cock like that!"'), 
	('What does one saggy boob say to the other saggy boob? "If we don\'t get some support, people will think we\'re nuts."'), 
	('What\'s the difference between your boyfriend and a condom? Condoms have evolved: They\'re not so thick and insensitive anymore.'), 
	('What\'s the difference between a G-spot and a golf ball? A guy will actually search for a golf ball!'), 
	('Why does it take 100 million sperm to fertilize one egg? Because they won\'t stop to ask directions.'), 
	('How do you embarrass an archaeologist? Give him a used tampon and ask him which period it came from.'), 
	('What does the receptionist at a sperm bank say as clients leave? "Thanks for coming!"'), 
	('What do you call a smiling Roman soldier with a piece of hair stuck between his front teeth? A glad-he-ate-her.'), 
	('What\'s long and hard and full of semen? A submarine!'),
    ('What did the clitoris say to the vulva?“It\'s all good in the hood!”'), 
	('My girlfriend asked me if I smoke after sex…I said I haven\'t looked.'), 
	('What do you call a person who doesn\'t masturbate?A liar.'), 
	('A worm crawls out of a pile of spaghetti…It says, “Damn, that was one hell of an orgy!”'), 
	('Sex is like a burrito…Don\'t unwrap or that baby\'s in your lap.'), 
	('A guy is sitting at the doctor\'s office.The doctor walks in and says, “I have some bad news. I\'m afraid you\'re going to have to stop masturbating.”“I don\'t understand, doc,” the patient says. “Why?”“Because,” the doctor says. “I\'m trying to examine you.”'), 
	('What\'s the difference between a G-spot and a clitoris?Men don\'t care.'), 
	('What are the three shortest words in the English language?Is it in?'), 
	('What does the sign on an out-of-business brothel say?“Beat it. We\'re closed!”'), 
	('Why does Dr. Pepper come in a bottle?Because his wife has passed away.'), 
	('Beer Bottle: “You break me, you get one year of bad luck!”Mirror: “You kiddin\' me? You break me, then y\'all get seven years of bad luck!”Condom: “Hahaha… (Condom walks off laughing)”'), 
	('What do you call a herd of cows masturbating?Beef strokin\' off!'), 
	('What\'s the difference between your penis and a bonus check?Someone\'s always willing to blow your bonus.'), 
	('What did the guy say when he got caught masturbating to an optical illusion?“It\'s not what it looks like!”'), 
	('Knock, knock.Who\'s there?Not someone.Not someone who?Not someone who will get you laid.'), 
	('How did you quit smoking?I decided to smoke only after sex.'), 
	('Do you want to hear a joke about my vagina?Never mind. You\'ll never get it!'), 
	('What did the banana say to the vibrator?“Why are you shaking? She\'s going to eat me!”'), 
	('Why is masturbation just like procrastination?It\'s all good until you realize you\'re only screwing yourself.'), 
	('Knock, knock.Who\'s there?Dewey!Dewey who?Dewey see a condom? It\'s dark in here!'), 
	('What\'s the difference between a tire and 365 used condoms?Ones a Goodyear. The other is a great year.'), 
	('The other day I was so frustrated I yelled out, “Fuck my life.”The neighbor heard, “Fuck my wife.”'), 
	('What\'s the difference between a G-spot and a golf ball?A man will actually search for a golf ball.'), 
	('What did the penis say to the vagina?“Don\'t make me cum in there!”'), 
	('Why did the dick go crazy?Someone was messing with his head.'), 
	('What\'s another name for a diaphragm?A trampoline for dicks.'), 
	('What does Popeye use as a lubricant?Olive Oyl.'), 
	('Why is Santa\'s sack so big?He only comes once a year.'), 
	('What\'s better than pansies on a piano?Tulips on your organ!'), 
	('What did the penis say to the condom?“Cover me, I\'m going in.”'), 
	('What did Adam say to Eve?“Stand back. I don\'t know how big this thing\'s gonna grow.”'), 
	('What do a penis and a Rubik\'s Cube have in common?The more you play with it, the harder it gets.'), 
	('What\'s the one difference between a pregnant woman and a lightbulb?You can unscrew the lightbulb.')
]

bot = Bot("!")

@bot.command(pass_context = True)
async def join(ctx):
	if (ctx.author.voice):
		channel = ctx.author.voice.channel
		await channel.connect()
	else:
		await ctx.send("You aren't in a voice channel.. otherwise I'd of said it.. bitch")

@bot.command(pass_context = True)
async def leave(ctx):
	if (ctx.voice_client):
		await ctx.guild.voice_client.disconnect()
		await ctx.send("I left the voice channel")

@bot.command(pass_context = True)
async def testTTS(ctx):
	if (ctx.author.voice):
		engine = pyttsx3.init()
		voices = engine.getProperty('voices')
		index = 0
		
		for voice in voices:
			print(f'index-> {index} -- {voice.name}')
			index +=1
			
		engine.runAndWait()

#@bot.command(pass_context = True)
#async def moan(ctx):
#	if (ctx.author.voice):
#		channel = ctx.author.voice.channel
#		vc = await channel.connect()
#		vc.play(discord.FFmpegPCMAudio(source="TTS_Files/Moan.mp3"))
#		
#		while vc.is_playing():
#			print("playing...")
#			 
#		await asyncio.sleep(2)
#		await ctx.guild.voice_client.disconnect()

@bot.command(pass_context = True)
async def gofuckyourself(ctx):
	if (ctx.author.voice):
		channel = ctx.author.voice.channel
		vc = await channel.connect()
		vc.play(discord.FFmpegPCMAudio(source="TTS_Files/GoFuckYourselfOlly.mp3"))
		
		while vc.is_playing():
			print("playing...")
			 
		await asyncio.sleep(2)
		await ctx.guild.voice_client.disconnect()

#@bot.command(pass_context = True)
#async def merkal(ctx):
#	if (ctx.author.voice):
#		channel = ctx.author.voice.channel
#		vc = await channel.connect()
#		vc.play(discord.FFmpegPCMAudio(source="TTS_Files/Merkal.mp3"))
#		
#		while vc.is_playing():
#			print("playing...")
#			 
#		await asyncio.sleep(2)
#		await ctx.guild.voice_client.disconnect()

@bot.command(pass_context = True)
async def ofcourse(ctx):
	if (ctx.author.voice):
		channel = ctx.author.voice.channel
		vc = await channel.connect()
		vc.play(discord.FFmpegPCMAudio(source="TTS_Files/OneMillionPercent.mp3"))
		
		while vc.is_playing():
			print("playing...")
			 
		await asyncio.sleep(2)
		await ctx.guild.voice_client.disconnect()

@bot.command(pass_context = True)
async def tip(ctx):
	if (ctx.author.voice):
		channel = ctx.author.voice.channel
		vc = await channel.connect()
		vc.play(discord.FFmpegPCMAudio(source="TTS_Files/Tip.mp3"))
		
		while vc.is_playing():
			print("playing...")
			 
		await asyncio.sleep(2)
		await ctx.guild.voice_client.disconnect()

@bot.command(pass_context = True)
async def nightroast(ctx):
	if (ctx.author.voice):
		channel = ctx.author.voice.channel
		vc = await channel.connect()
		vc.play(discord.FFmpegPCMAudio(source="TTS_Files/NightRoast.mp3"))
		
		while vc.is_playing():
			print("playing...")
			 
		await asyncio.sleep(2)
		await ctx.guild.voice_client.disconnect()

@bot.command(pass_context = True)
async def smaller(ctx):
	if (ctx.author.voice):
		channel = ctx.author.voice.channel
		vc = await channel.connect()
		vc.play(discord.FFmpegPCMAudio(source="TTS_Files/Smaller.mp3"))
		
		while vc.is_playing():
			print("playing...")
			 
		await asyncio.sleep(2)
		await ctx.guild.voice_client.disconnect()

@bot.command(pass_context = True)
async def dirtyjoke(ctx):
    dirtyJokeId = random.randint(0, len(jokeList)-1)

    response = f'|| {jokeList[dirtyJokeId]} || {ctx.author.mention}'
    await ctx.send(response)

    if (ctx.author.voice):
        channel = ctx.author.voice.channel
        vc = await channel.connect()

        mp3filename = f"TTS_Files/{ctx.author.name}-{time.time()}.mp3"
        
		#engine = pyttsx3.init()
        #voices = engine.getProperty('voices')
        #engine.setProperty('voice', voices[17].id)
        #engine. setProperty("rate", 140)
        #engine.save_to_file(jokeList[dirtyJokeId], mp3filename)
        #engine.runAndWait()
        tts = gTTS(jokeList[dirtyJokeId], lang='en', tld='co.in')
        tts.save(mp3filename)

        vc.play(discord.FFmpegPCMAudio(source=mp3filename))

        while vc.is_playing():
            print("playing...")

        await asyncio.sleep(3)
        await ctx.guild.voice_client.disconnect()

bot.run(TOKEN)