# bot_7 by KARIM

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import os
import chalk

api = str(os.environ.get('RIOT_KEY'))

#startup_extensions = ["Music"]
bot2 = commands.Bot(command_prefix='.')
bot = commands.Bot(command_prefix='7_')

@bot.event
async def on_ready():
	print("je suis pret")
	print("Je m'appele " + bot.user.name)
	print("mon id est " + bot.user.id)
	
@bot2.event
async def on_ready():
	print("je suis pret")
	print("Je m'appele " + bot.user.name + "_2")
	print("mon id est " + bot.user.id + "_2")
	
#class Main_Commands():
	#def __init__(self, bot):
		#self.bot = bot

@bot.command(pass_context = True)
async def ping(ctx):
	await bot.say(":ping_pong: pong!!")

@bot.command(pass_context = True)
async def bon(ctx):
	await bot.say("jour")
	
@bot.command(pass_context = True)
async def salut(ctx, user: discord.Member):
	await bot.say("Bonjour {} :wave:".format(user.name))
	
@bot.command(pass_context = True)
async def origine(ctx):
	await bot.say("Mon code a été réaliser par @KARIM#9286")
	
@bot2.command(pass_context = True)
async def music(ctx):
	await bot.say("You have to be in the Music vocal chanel to listen music.")
#if __name__ == "__main__":
	#for extension in startup_extensions:
		#try:
			#bot.load_extension(extension)
		#except Exception as e:
			#exc = '{}: {}'.format(type(e).__name__, e)
			#print('Failed to load extension {} \n {}'.format(extension, exc))


bot.run(str(os.environ.get('BOT_TOKEN')))

