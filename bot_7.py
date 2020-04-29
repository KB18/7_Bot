# bot_7 by KARIM

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import os
from vote import *
from random import randint
import youtube_dl
#Code fait pour l'occasion
import recherche_youtube
import recherche_youtube_titre
from embedEnvoi import envoi
import recherche_horaire_priere
import recherche_horaire_priere_ramadan

api = str(os.environ.get('RIOT_KEY'))
bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

version_bot = "17.5"

#channel = "test_bot"
vote = None
players = {}
queues = {}
queues_titre = {}
player = None

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="$help"))
	print("je suis pret")
	print("Je m'appele " + str(bot.user.name))

@bot.event
async def on_command_error(ctx, error):
	titre = ":x: ERREUR :interrobang:"
	texte = ""
	if isinstance(error, commands.MissingRequiredArgument):
		texte = "il manque un argument lors de ton utilisation de cette commande !!!!\n"
		texte += "tu devrais utiliser la commande help pour savoir comment utiliser cette commande"
	elif isinstance(error, commands.CommandNotFound):
		texte = "Commande Invalide ou Inexistante"
	else:
		print(error)
		texte = "ERREUR : JE NE BLAGUE PAS ERREUR OHOHOOHOHO DIT LE AU PLUS VITE AU FRERO KARIM"

	'''------embed pour affichage erreur--------'''
	await envoi(ctx, titre, texte)

'''------------------------------------------comptabilisation des votes-------------------------------------'''
@bot.event
async def on_reaction_add(reaction, user):
	global vote
	'''print(channel_actu)
	print(channel)
	'''

	if (vote != None):
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
async def votes(ctx, contenue_txt_vote:str):

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
		embed.set_author(name="Les differente utilisation de cette commande sont : ")
		await ctx.send(embed=embed)

	elif(contenue_txt_vote == "close"):
		if vote != None and ctx.message.author.name == vote.get_Auteur():
			texte_fin_vote = vote.closeVote()
			await ctx.send(texte_fin_vote)
			vote = None
		else:
			await ctx.send(":boom: :fire: :no_entry_sign: :no_entry: ALERTE :no_entry: :no_entry_sign: :fire: :boom: : \n Quelqu'un a essayé d'attaquer la démocratie\n VERMINE NE RECOMMENCER PLUS JAMAIS \n LA DEMOCRATIE VAINCRA \n GLOIRE A LA NATION")
			await ctx.send("------------------\nNE RECOMMENCE PAS !!!! \nje t'ai a l'oeil {} !!".format(str(ctx.message.author.name)))
	else:	
		if(vote != None):
			await ctx.send('VOTE actuellement en cours !!')
		else:
			vote = Vote(str(contenue_txt_vote), str(ctx.message.author.name))
			msg = await ctx.send("LE VOTE DE LA NATION\n"+contenue_txt_vote)
			reactions = ['✅', '❎']
			for emoji in reactions:
				await msg.add_reaction(emoji)

'''------------------------------------------commande autre-------------------------------------'''
@bot.command()
async def presentation(ctx):
	await ctx.send("SALUTATION CAMARADES, JE M'APPELLE MIRAK ET J'AI REJOINT VOS RANGS POUR VOUS EPAULEZ DANS VOTRE COMBAT !!")

@bot.command()
async def ping(ctx):
	await ctx.send(":ping_pong: pong !! ha bah je sais pas encore faire sa car mon dev et pas trés malin mais un jour ki sais !!")

@bot.command()
async def bon(ctx):
	await ctx.send("jour ! MDR tu t'y attendais pas hein :joy:")
	
@bot.command()
async def salut(ctx):
	await ctx.send("Salutation, camarade {} !! L'UNION FAIT LA FORCE, \nHEUREUX QUE TU ES REJOINT NOS RENDS, \nENSEMBLE NOUS NOUS BATTRONS ET VAINCRONS POUR LE BIEN DE L'HUMANITÉ".format(str(ctx.message.author.name)))
	
@bot.command()
async def origine(ctx):
	await ctx.send("Mon code a été réaliser par KARIM aka KARIM LE FONDATEUR")

@bot.command()
async def version(ctx):
	await ctx.send("Version "+version_bot+" ! camarade {}".format(str(ctx.message.author.name)))

@bot.command()
async def orthographe(ctx):
	await ctx.send("fait pas attention a mon orthographe elle va s'ameliorer un jour")

@bot.command()
async def code(ctx, lang, *, content=""):
	if lang == "help" and content == "":
		texte = "$codes <nom du code> <code brut> : permet d'envoyer du code de manière propre (coloré, etc...)"
		embed = discord.Embed(
			description = texte,
			colour = discord.Colour.green()
		)
		embed.set_author(name="Les differente utilisation de cette commande sont : ")
		await ctx.send(embed=embed)
	else:
		await ctx.channel.purge(limit=1)
		texte = " ```"+str(lang)+"\n"
		texte += content
		texte += "\n```"
		texte += "*** Ecrit par ***"+str(ctx.message.author.mention)
		await ctx.send(texte)


@bot.command()
async def insulte(ctx, message):
	table_isultes = []
	nb_alea = randint(0, 310)
	with open("insulte.txt", "r") as f:
		for insulte in f.readlines():
			table_isultes.append(insulte)
	msg = str(message)+"  ->  " + str(table_isultes[nb_alea])
	msg += "cela a été prouvé"
	await ctx.send(msg)

@bot.command()
async def trad(ctx, message):
	pass	

@bot.command()
async def spammention(ctx, nb:int, message):
	auteur = ctx.message.author.name
	avatar = ctx.message.author.avatar_url
	await ctx.send("Spam commence")
	if nb < 1000:
		for i in range(int(nb)):
			await ctx.send(message)
		await envoi(ctx, titre="Spammage", texte=message, auteur=auteur, avatar=avatar, desti="spam")
	else:
		await envoi(ctx, titre="Spammage", texte="Trop de spam tu le spam", auteur=auteur, avatar=avatar, desti="spam")

@bot.command()
async def purge(ctx, nb):
		auteur = ctx.message.author.name
		if str(auteur) == "KARIM":
			await ctx.channel.purge(limit=int(nb))
		else:
			await ctx.send("VOUS N'ETES pas autorisé")
			
@bot.command()
async def horairepriere(ctx):
	nom_priere, horaire_priere = recherche_horaire_priere.main()
	texte = ""
	for i in range(6):
		texte += "---------- "+nom_priere[i]+" ---------- : \n"
		texte += "\t"+horaire_priere[i]+"\n"
	await envoi(ctx, ":mosque: HORAIRES DE PRIÈRES :mosque:", texte, auteur="[Mosquée de Lyon](http://mosquee-lyon.org/)", desti="horairepriere")

@bot.command()
async def horairepriereramadan(ctx):
	nom_priere, horaire_priere, info_bonus = recherche_horaire_priere_ramadan.main()
	texte = ""
	for j in range(3):
		texte += info_bonus[j]+"\n"
	for i in range(6):
		texte += "---------- "+nom_priere[i]+" ---------- : \n"
		texte += "\t"+horaire_priere[i]+"\n"
	await envoi(ctx, ":mosque: HORAIRES DE PRIÈRES :mosque:", texte, auteur="[Islamic Finder](http://"+info_bonus[4]+")", desti="horairepriere")

@bot.command()
async def ftour(ctx):
	pass
'''------------------------------------------commande pour la musique-------------------------------------'''
def suppr_apartir(txt, c):
	tmp =""
	for i in txt:
		tmp+=i
		if i == c :
			return tmp
	return tmp
def suppr_apartir_reverse(txt, c):
    tmp = ""
    tmp_propre=""
    i = len(txt) - 1
    while (i > 0):
        if txt[i] == c:
            break
        tmp += txt[i]
        i-=1
    j = len(tmp) - 1
    while (j >= 0):
        tmp_propre += tmp[j]
        j -= 1
    return tmp_propre

def check_queue(ctx, guild):
	i = guild.id
	if queues[i] != []:

		queues[i].pop(0)
		queues_titre[i].pop(0)

		if queues[i] != []:
			url = queues[i][0]
			titre = queues_titre[i][0]

			joue_url(ctx, guild, url)

		
def add_queue(ctx, guild, url):
	if guild.id in queues and queues[guild.id] != []:
		queues[guild.id].append(url)
		queues_titre[guild.id].append(recherche_youtube_titre.main(url))

	else:
		queues[guild.id] = [url]
		queues_titre[guild.id] = [recherche_youtube_titre.main(url)]

		joue_url(ctx, guild, url)
		

def cherche_mot(txt, mot):
	succes = False
	for i in range(len(txt)):
		nb_suite = 0
		if txt[i] == mot[0]:
			nb_suite +=1
			for j in range(len(mot)):
				if i+j < len(txt):
					if txt[i+j] == mot[j] and j != 0:
						nb_suite +=1
		if nb_suite == len(mot):
			succes = True
	return succes

def commence_par(txt, mot):
	succes = True
	if(len(txt)<len(mot)):
		succes = False
	else:
		for i in range(len(mot)):
			if txt[i] != mot[i]:
				succes = False
	return succes

def se_termine_par(txt, mot):
	succes = True
	if(len(txt)<len(mot)):
		succes = False
	else:
		i = len(mot) - 1
		j = len(txt) - 1
		while (i > 0):
			if txt[j] != mot[i]:
				return False
			j-=1
			i-=1
	return succes


	

def non_playlist(url):
	succes = False
	block_playlist = "list"
	#blocage des playlist par detection de la presence du mot "list" dans l'url
	succes = cherche_mot(url, block_playlist)
	return succes

def lien_youtube_valide(url):
	lien_valide = "https://www.youtube.com/watch?v="
	succes = commence_par(url, lien_valide)
	return succes




def telecharge_musique(url, guild, nb=0):
	#telecharge musique

	#suppr tout fichier mp3 different des song
	with os.scandir("./") as fichiers:
		for fichier in fichiers:
			if commence_par(str(fichier.name), 'song'+str(guild.id)+'nb') == False and se_termine_par(fichier.name, '.mp3'):
				os.remove(fichier.name)

	ydl_opts = {
		'audioformat' : "mp3",
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])

	with os.scandir("./") as fichiers:
		for fichier in fichiers:

			if se_termine_par(fichier.name, ".mp3"):
				print("trouver")
				os.rename(fichier, 'song'+str(guild.id)+'nb'+str(nb)+'nb.mp3')
				break




def joue_url(ctx, guild, url):
	with os.scandir("./") as fichiers:
		for fichier in fichiers:
			if fichier.name == 'song'+str(guild.id)+'nb0nb.mp3':
				os.remove('song'+str(guild.id)+'nb0nb.mp3')

	#jouer de la musique / dl si pas deja dl en avance
	telecharge_musique(url, guild)


	players[guild.id].play(discord.FFmpegPCMAudio('song'+str(guild.id)+'nb0nb.mp3'), after=lambda e: check_queue(ctx, guild))
		
	print('done')

async def join(ctx, guild):
		# join un channel vocal ou pas
	connecter_channel_vo = False
	for x in bot.voice_clients:
		if(x.guild == ctx.message.guild):
			connecter_channel_vo = True
	if connecter_channel_vo == False:
		channel = ctx.message.author.voice.channel
		player = await channel.connect()
	#ajout du player si nv
	if connecter_channel_vo == False :
		players[guild.id] = player
		#teste si fichier music deja existant si oui suppression

		'''-------------------------obselete-------------------------------------------'''
		with os.scandir("./") as fichiers:
			for fichier in fichiers:
				if fichier.name == 'song'+str(guild.id)+'.mp3':
					os.remove('song'+str(guild.id)+'.mp3')


@bot.command()
async def joue(ctx, url, *, content=""):
	#variable utile dans tout la def
	auteur = ctx.message.author.name
	avatar_auteur = ctx.message.author.avatar_url
	guild = ctx.message.guild
	titre = "Music"

	if lien_youtube_valide(str(url)) :

		if non_playlist(url) == True:
			url=suppr_apartir(url, "&")
			await ctx.send("C'est une playliste seul la première a été récuperé")


		await join(ctx, guild)

		add_queue(ctx, guild, url)


		await envoi(ctx, titre, "Ajout de : \n"+str(recherche_youtube_titre.main(url)), auteur, avatar_auteur, "music")

	else :
		recherche_music = str(url)+" "+content
		url_trouver, titreMusic = recherche_youtube.main(recherche_music)
		url_trouver = "https://www.youtube.com"+url_trouver

		if non_playlist(url_trouver) == True:
			url_trouver=suppr_apartir(url_trouver, "&")
			await ctx.send("C'est une playliste seul la première a été récuperé")

		await join(ctx, guild)

		add_queue(ctx, guild, url_trouver)


		await envoi(ctx, titre, "Ajout de : ["+titreMusic+"]("+url_trouver+")", auteur, avatar_auteur, "music")
		

@bot.command()
async def pause(ctx):
	guild = ctx.message.guild
	if (players[guild.id] != None):
		players[guild.id].pause()

@bot.command()
async def resume(ctx):
	guild = ctx.message.guild
	if (players[guild.id] != None):
		players[guild.id].resume()
@bot.command()
async def next(ctx):
	guild = ctx.message.guild
	if (players[guild.id] != None):
		players[guild.id].stop()

@bot.command()
async def queue(ctx):
	guild = ctx.message.guild
	texte = ""
	titreM = "Music Queue"
	for titre in queues_titre[guild.id]:
		texte += titre+"\n"
	await envoi(ctx, titreM, texte)

"""@bot.command()
async def playlist(ctx, categorie):
"""	
@bot.command()
async def purgeQueue(ctx):
	guild = ctx.message.guild
	if (players[guild.id] != None):
		players[guild.id].stop()

		queues[guild.id] = []
		queues_titre[guild.id] = []

		with os.scandir("./") as fichiers:
			for fichier in fichiers:
				if se_termine_par(fichier.name, ".mp3"):
					os.remove(fichier)

@bot.command()
async def arrete(ctx):
	guild = ctx.message.guild
	if (players[guild.id] != None):
		players[guild.id].stop()
		guild_voice = ctx.message.guild.voice_client
		await guild_voice.disconnect()

		queues[guild.id] = []
		queues_titre[guild.id] = []

		with os.scandir("./") as fichiers:
			for fichier in fichiers:
				if se_termine_par(fichier.name, ".mp3"):
					os.remove(fichier)


'''------------------------------------------commande help-------------------------------------'''
@bot.command()
async def help(ctx):
	texte = "---------------------\n"
	texte += "ping\n"
	texte += "bon\n"
	texte += "salut\n"
	texte += "origine\n"
	texte += "votes\n"
	texte += "version\n"
	texte += "orthographe\n"
	texte += "presentation\n"
	texte += "code\n"
	texte += "joue\n"
	texte += "arrete\n"
	texte += "pause\n"
	texte += "resume\n"
	texte += "next\n"
	texte += "purgeQueue\n"
	texte += "insulte"
	texte += "spammention\n"
	texte += "horairepriere\n"
	texte += "horairepriereramadan\n"
	texte += "---------------------\n"

	titre = 'Commande HELP'

	await envoi(ctx, titre, texte, "@KARIM#9286 aka KARIM LE FONDATEUR", desti="help")

bot.run(str(os.environ.get('BOT_TOKEN')))

