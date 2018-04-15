# bot_7 by KARIM

import discord
from discord.ext import commands
from discord.ext.commands import Bot 
import asyncio

api = str(os.environ.get('RIOT_KEY'))

bot = commands.Bot(command_prefix='7_')

@bot.event
async def on_ready():
	print("je suis pret")
	print("Je m'appele " + bot.user.name)
	print("mon id est " + bot.user.id)

@bot.command(pass_context = True)
async def ping(ctx):
	await bot.say(":ping_pong: pong!!")


bot.run(str(os.environ.get('BOT_TOKEN')))

