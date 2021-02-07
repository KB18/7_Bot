# bot_7 by KARIM

import discord
from discord.channel import VoiceChannel
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import os
from vote import *
from random import randint
import youtube_dl
from datetime import datetime
from time import sleep
from random import randint
#Code fait pour l'occasion
import recherche_youtube
import recherche_youtube_titre
from embedEnvoi import envoi
import recherche_horaire_priere
import recherche_horaire_priere_ramadan
import recherche_gif_alea

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

version_bot = "21"

#channel = "test_bot"
vote = None
players = {}
queues = {}
queues_titre = {}
player = None
channel_horaire_priere = 'heures-de-la-priere'
voc_horaire_priere = 'Adhan'
role_horaire_priere = "muslim"

jour_actu = 1
mois_actu = 1

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
		texte += "tu devrais utiliser la commande help pour savoir comment utiliser cette commande\n"
		texte += "(si l'aide existe sinon bon  courage !!)\n"
	elif isinstance(error, commands.CommandNotFound):
		texte = "Commande Invalide ou Inexistante"
	else:
		print(error)
		texte = "ERREUR : JE NE BLAGUE PAS ERREUR OHOHOOHOHO DIT LE AU PLUS VITE AU FRERO KARIM"

	'''------embed pour affichage erreur--------'''
	await envoi(ctx, titre, texte)


async def time_check():
	global jour_actu, mois_actu
	nom_priere, horaire_priere, info_bonus = recherche_horaire_priere_ramadan.main() 
	horaire_priere = clear_time(horaire_priere)
	while True:
		now = datetime.now()

		if now.day != jour_actu or now.month != mois_actu:
			jour_actu = now.day
			mois_actu = now.month
			nom_priere, horaire_priere, info_bonus = recherche_horaire_priere_ramadan.main()
			horaire_priere = clear_time(horaire_priere)

		await verificateurHoraire(now.hour, now.minute, nom_priere, horaire_priere)

		await asyncio.sleep(3)

def clear_time(liste):
	for tmp in liste:
		temps = ""
		for i in range(tmp):
			if i == 5:
				break
			temps += tmp[i]
		if tmp[6] == 'P':
			temps[0] = '1'
			temps[1] = str(int(temps[1]) + 2)
		return temps


def conv_temp(tmp):
	if tmp < 10:
		tmp = "0"+str(tmp)
	return str(tmp)

async def verificateurHoraire(heure, minute, nom_priere, horaire_priere):
	global jour_actu
	heure = conv_temp(heure)
	minute = conv_temp(minute)
	#verif heure
	if heure+":"+minute in horaire_priere:
		#trouve index
		for i in range(len(horaire_priere)):
			if heure+":"+minute == horaire_priere[i]:
				
				#trouve serv
				for guild in bot.guilds:
					#text
					#trouve channel
					for channel in guild.text_channels:
						if channel.name == channel_horaire_priere:
							#message et suppr
							await channel.send(str(nom_priere[i]))
							#mention
							for role in guild.roles:
								if role_horaire_priere == role.name:
									await channel.send(role.mention)

							horaire_priere.pop(i)
							nom_priere.pop(i)

					#audio
					voc_ADHAN = None
					for vocal in guild.voice_channels:
						if vocal.name == voc_horaire_priere:
							voc_ADHAN = vocal
						if voc_ADHAN != None:
							for voc in guild.voice_channels:
								if voc.members != None:
									for membre in voc.members:
										if discord.utils.get(membre.roles, name=role_horaire_priere):
											await membre.move_to(voc_ADHAN)
							try:
								await voc_ADHAN.connect()
							except:
								print("deja co")
							finally:
								nb = randint(0, 2)
								if nb not in [0,1,2]:
									nb = 0
								voice = discord.utils.get(bot.voice_clients, guild=guild)
								voice.play(discord.FFmpegPCMAudio("adhan_"+nb+".mp3"))
				break


				


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
async def votes(ctx, *, contenue_txt_vote:str=""):

	contenue_txt_vote = str(contenue_txt_vote)
	global vote
	if(contenue_txt_vote == ""):
		await ctx.send('Erreur')

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
		auteur = ctx.message.author
		if str(auteur) == "KARIM#9286":
			await ctx.channel.purge(limit=int(nb))
			await ctx.send("Ce fut un plaisir de vous aider Maréchal "+str(ctx.message.author.name))
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

#standby
@bot.command()
async def muslimMission(ctx):
	guild = ctx.message.guild
	category = None
	role = None

	#role
	if discord.utils.get(guild.roles, name=role_horaire_priere) == None :
		role = await guild.create_role(name=role_horaire_priere, colour=discord.Colour(0x00ff00))
		await ctx.send("Role pret akhi !! ")
		print("role")
	else:
		for rol in  guild.roles:
			if rol.name == role_horaire_priere:
				role = rol
		await ctx.send("Role deja pret akhi !! ")

	#catégorie
	if  discord.utils.get(guild.categories, name=channel_horaire_priere) == None:
		category = await guild.create_category(channel_horaire_priere)
		for rolx in guild.roles:
			if rolx.name == "@everyone":
				await category.set_permissions(rolx, read_messages=False)
		await category.set_permissions(role, read_messages=True)
		print("cat")
		await ctx.send("Catégorie pret akhi !! ")
	else:
		for cat in  guild.categories:
			if cat.name == channel_horaire_priere:
				category = cat
		await ctx.send("Catégorie deja pret akhi !! ")

	#channel
	if discord.utils.get(guild.text_channels, name=channel_horaire_priere) == None:
		await guild.create_text_channel(channel_horaire_priere, category=category)
		await ctx.send("Channel pret akhi !! ")
		print("channel")
	else:
		await ctx.send("Channel deja pret akhi !! ")

	if discord.utils.get(guild.voice_channels, name=voc_horaire_priere) == None:
		await guild.create_voice_channel(voc_horaire_priere, category=category)
		await ctx.send("Channel vocal pret akhi !! ")
		print("channel")
	else:
		await ctx.send("Channel vocal deja pret akhi !! ")

	

@bot.command()
async def gif(ctx, *, msg:str):
	titre ="**GIF**"
	texte = str(msg)
	auteur = ctx.message.author.name
	auteur_avatar = ctx.message.author.avatar_url
	img = recherche_gif_alea.main(texte)
	if img != "gifs introuvable":
		await envoi(ctx, titre, auteur=auteur, avatar=auteur_avatar, desti="gif", image=img)
	else:
		await ctx.send("OHHHHHHHHHHHHH t'es debilos ou quoi ?? pourquoi tu roule ta tete sur ton clavier ???")

@bot.command()
async def pin(ctx):
	channel = ctx.message.channel
	auteur_id = ctx.message.author.id
	await ctx.channel.purge(limit=1)
	
	msg = await channel.history().find(lambda msg: msg.author.id == auteur_id)

	if(msg != None):
		await msg.pin()
	else:
		await ctx.send("ahhhhhhhhhh impossible de trouver ton dernier message ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

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
		await ctx.send("Il me faut un lien pour jouer l'audio !!")
		

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
async def help(ctx, *, content=""):
	content = str(content)
	titre = 'Commande HELP '

	if content == "code":
		texte = "$codes <nom du code> <code brut> : permet d'envoyer du code de manière propre (coloré, etc...)"
		await envoi(ctx, titre=titre+content, texte=texte,  desti="help_commande")

	elif content == "votes":
		texte = "$votes <intituler du vote entre guillemets> : permet de creer un vote\n"
		texte += "$votes <close> :  qui permet de fermer un vote et d'obtenir les resultats"
		await envoi(ctx, titre=titre+content, texte=texte,  desti="help_commande")

	elif content == "pin":
		texte = "$pin : permet d'epingler le dernier message que vous avez envoyer\n"
		await envoi(ctx, titre=titre+content, texte=texte,  desti="help_commande")

	else:
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
		texte += "insulte\n"
		texte += "spammention\n"
		texte += "horairepriere\n"
		texte += "horairepriereramadan\n"
		texte += "gif\n"
		texte += "pin\n"
		texte += "deploimentdansletheatredoperation\n"
		texte += "---------------------\n"


		await envoi(ctx, titre, texte, "@KARIM#9286 aka KARIM LE FONDATEUR", desti="help")

bot.loop.create_task(time_check())

bot.run(str(os.environ.get('BOT_TOKEN')))


