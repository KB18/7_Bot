# bot_7 by KARIM

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import os

api = str(os.environ.get('RIOT_KEY'))

#startup_extensions = ["Music"]
bot = commands.Bot(command_prefix='*')

@bot.event
async def on_ready():
	print("je suis pret")
	print("Je m'appele " + bot.user.name)
	print("mon id est " + bot.user.id)
	
#class Main_Commands():
	#def __init__(self, bot):
		#self.bot = bot

@bot.command()
async def ping(ctx):
	await bot.say(":ping_pong: pong!!")

@bot.command()
async def bon(ctx):
	await bot.say("jour")
	
@bot.command()
async def salut(ctx, user: discord.Member):
	await bot.say("Bonjour {} :wave:".format(user.name))
	
@bot.command()
async def origine(ctx):
	await bot.say("Mon code a été réaliser par KARIM")
	
@bot.command()
async def music(ctx):
	await bot.say("pas encore coder.")


bot.run(str(os.environ.get('BOT_TOKEN')))

