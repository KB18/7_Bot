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
	if auteur != "" and avatar != "" and desti == "spam":
		embed.set_footer(text="Ce spammage vous a été offert par : "+auteur, icon_url=avatar)
	if auteur != "" and desti == "horairepriere":
		embed.add_field(name="Source : ", value=auteur, inline=False)

	await ctx.send(embed=embed)