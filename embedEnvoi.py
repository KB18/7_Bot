import discord
import asyncio
async def envoi(ctx, titre, texte="", auteur="", avatar="", desti="", image=""):
	
	embed = discord.Embed(
		description = texte,
		colour = discord.Colour.blue(),
		title = "**"+titre+"**"
	)
	if auteur != "" and avatar != "" and desti == "music":
		embed.set_footer(text="Ajouter par : "+auteur, icon_url=avatar)

	if auteur != "" and desti == "help":
		embed.set_footer(text="Inventé et codé par : "+auteur)

	if auteur != "" and avatar != "" and desti == "spam":
		embed.set_footer(text="Ce spammage vous a été offert par : "+auteur, icon_url=avatar)

	if auteur != "" and desti == "horairepriere":
		embed.add_field(name="Source : ", value=auteur, inline=False)
	if auteur != "" and desti =="gif" and image !="":
		embed.set_image(url=image)
		embed.set_footer(text="Affiché par "+auteur, icon_url=avatar)

	await ctx.send(embed=embed)