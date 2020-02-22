# bot_7 by KARIM

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import os
from vote import*

api = str(os.environ.get('RIOT_KEY'))
bot = commands.Bot(command_prefix='$')
bot.remove_command('help')
channel = "test_bot"
vote = None
players = {}

@bot.event
async def on_ready():
	print("je suis pret")
	print("Je m'appele " + str(bot.user.name))
	print("mon id est " + str(bot.user.id))

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		texte = "il manque un argument !!!!\n"
		texte += "tu devrais utiliser la commande help pour savoir comment utiliser cette commande"
		await ctx.send(texte)
	else:
		print(error)
'''------------------------------------------comptabilisation des votes-------------------------------------'''
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
		elif(reaction.emoji == "❎"):
			if(vote.aDejaVoter(str(user.name))!=True and str(user.name) != str(bot.user.name)):
				vote.addNon()
				vote.ajtVotant(str(user.name))
		else:
			print("emote pas reconnu")
	else:
		print("pas dans le bon channel")

'''------------------------------------------commande pour le vote-------------------------------------'''
@bot.command()
async def votes(ctx, contenue_txt_vote):

	contenue_txt_vote = str(contenue_txt_vote)
	global vote
	if(contenue_txt_vote == ""):
		await ctx.send('Erreur')
	elif(contenue_txt_vote == "help"):
		texte = " votes <intituler du vote entre guillemets> : permet de creer un vote\n"
		texte += "votes <close> :  qui permet de fermer un vote et d'obtenir les resultats"
		embed = discord.Embed(
			description = texte,
			colour = discord.Colour.green()
		)
		embed.set_author(name="Les differrente utilisation de cette commande sont : ")
		await ctx.send(embed=embed)

	elif(contenue_txt_vote == "close"):
		if vote != None:
			texte_fin_vote = vote.closeVote()
			await ctx.send(texte_fin_vote)
			vote = None
		else:
			await ctx.send(":boom: :fire: :no_entry_sign: :no_entry: ALERTE :no_entry: :no_entry_sign: :fire: :boom: : Quelqu'un a essayé d'attaquer la démocratie\n VERMINE NE RECOMMENCER PLUS JAMAIS \n LA DEMOCRATIE VAINCRA \n GLOIRE A LA NATION")

	else:	
		vote = Vote(str(contenue_txt_vote))
		msg = await ctx.send("LE VOTE DE LA NATION\n"+contenue_txt_vote)
		reactions = ['✅', '❎']
		for emoji in reactions:
			await msg.add_reaction(emoji)

'''------------------------------------------commande autre-------------------------------------'''
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
'''------------------------------------------commande pour la musique-------------------------------------'''


'''------------------------------------------commande help-------------------------------------'''
@bot.command()
async def help(ctx):
	texte = "ping\n"
	texte += "bon\n"
	texte += "salut\n"
	texte += "origine\n"
	texte += "votes\n"
	embed = discord.Embed(
		description = texte,
		colour = discord.Colour.green()
	)
	embed.set_author(name='Commande HELP')

	await ctx.send(embed=embed)

bot.run(str(os.environ.get('BOT_TOKEN')))
