# bot_7 by KARIM

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import os
from vote import*

api = str(os.environ.get('RIOT_KEY'))
bot = commands.Bot(command_prefix='*')
channel = "test_bot"
vote = None

@bot.event
async def on_ready():
	print("je suis pret")
	print("Je m'appele " + str(bot.user.name))
	print("mon id est " + str(bot.user.id))

@bot.event
async def on_command_error(error, ctx):
	print(ctx)

@bot.event
async def on_reaction_add(reaction, user):
	global channel
	global vote
	channel_actu = reaction.message.channel
	'''print(channel_actu)
	print(channel)'''

	if (str(channel_actu) == str(channel) and vote != None):
		print(reaction.emoji)

		''' on ajoute 1 a la var oui de l obj vote'''
		if (reaction.emoji == "✅"):
			if (vote.aDejaVoter(str(user.name))!=True and str(user.name) != str(bot.user.name)):
				vote.addOui()
				vote.ajtVotant(str(user.name))
				'''print("+1")
				print(vote.get_Nb_oui())
				print(vote.get_IdVote())'''
		elif(reaction.emoji == "❎"):
			if(vote.aDejaVoter(str(user.name))!=True and str(user.name) != str(bot.user.name)):
				vote.addNon()
				vote.ajtVotant(str(user.name))
				'''print("-1")
				print(vote.get_Nb_non())
				print("nb vote total : "+str(vote.get_Nb_vote()))
				print(vote.get_IdVote())'''
		else:
			print("emote pas reconnu")
	else:
		print("pas dans le bon channel")


@bot.command()
async def vote(ctx, contenue_txt_vote):

	contenue_txt_vote = str(contenue_txt_vote)
	global vote
	if(contenue_txt_vote == ""):
		await ctx.send('Erreur')
	elif(contenue_txt_vote == "help"):

		await ctx.send('pas encore coder donc pas encore prets a aider la vie est dur')
		await ctx.send('		{embed: {color: 3447003,description: "**Voici les commandes du bot :**\n !help pour afficher les commandes"\}\}')
	elif(contenue_txt_vote == "close"):
		if vote != None:
			texte_fin_vote = vote.closeVote()
			await ctx.send(texte_fin_vote)
			vote = None
		else:
			await ctx.send(":no_entry: :no_entry_sign: :fire: :boom: ALERTE :no_entry: :no_entry_sign: :fire: :boom: : Quelqu'un a essayé d'attaquer la démocratie\n VERMINE NE RECOMMENCER PLUS JAMAIS \n LA DEMOCRATIE VAINCRA \n GLOIRE A LA NATION")

	else:	
		vote = Vote(str(contenue_txt_vote))
		msg = await ctx.send("LE VOTE DE LA NATION\n"+contenue_txt_vote)
		reactions = ['✅', '❎']
		for emoji in reactions:
			await msg.add_reaction(emoji)


@bot.command()
async def ping(ctx):
	await ctx.send(":ping_pong: pong!!")

@bot.command()
async def bon(ctx):
	await ctx.send("jour")
	
@bot.command()
async def salut(ctx, user: discord.Member):
	await ctx.send("Bonjour {} :wave:".format(user.name))
	
@bot.command()
async def origine(ctx):
	await ctx.send("Mon code a été réaliser par KARIM")
	
@bot.command()
async def music(ctx):
	await ctx.send("pas encore coder.")


bot.run(str(os.environ.get('BOT_TOKEN')))
