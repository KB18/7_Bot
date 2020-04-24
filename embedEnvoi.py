import discord
import asyncio
async def envoi(ctx, titre, texte, auteur="", avatar="", desti=""):
	
	embed = discord.Embed(
		description = texte,
		colour = discord.Colour.blue(),
		title = "**"+titre+"**"
	)
	if auteur != "" and avatar != "" and desti == "music":
		embed.set_footer(text="Ajouter par : "+auteur, icon_url=avatar)
	if auteur != "" and desti == "help":
		embed.set_footer(text="Inventé et codé par : "+auteur)
	if auteur != "" and desti == "spam":
		embed.set_footer(text="Cet personne est entrain de spammer : "+auteur)

	await ctx.send(embed=embed)