import os
import discord
import requests


from discord import Webhook, RequestsWebhookAdapter

from datetime import datetime
import time
from dotenv import load_dotenv

default_intents = discord.Intents.default()
default_intents.members = True

load_dotenv(dotenv_path="config");

client = discord.Client(intents=default_intents)

channel_config_id = 845295311311470593

#config_channel = client.get_channel(845295311311470593)

# config_channel	les pseudos doivent être formatés comme suit
#			sur plusieurs lignes ou plusieurs messages
#
# .<nom de la catégorie du jdr> : <pseudo>

now = time.localtime(time.time())

@client.event
async def on_ready():
	print(time.strftime("%d/%m/%y %H:%M", now))
	print("Le bot est prêt");

def remove_prefix(_str, prefix):
	if _str.startswith(prefix):
		return _str[len(prefix):]
	else:
		return _str

def aff_log(data):
	print(data)
	my_file = open("log_mille_mots.txt", "a")
	my_file.write(data)
	my_file.write("\n")
	my_file.close()

async def whats_your_name(member, jdr_name):
	aff_log("jdr_name : " + jdr_name)
	config_channel = client.get_channel(channel_config_id)
	default = member.name
	async for config_pseudo in config_channel.history():
		if (member == config_pseudo.author):
			source_names = config_pseudo.content.split("\n")
			for each_jdr in source_names:
				if (each_jdr.startswith(".") and each_jdr.find(" : ") > 1):
					tab_pseudo = each_jdr.split(" : ")
					aff_log("\ntab_pseudo : '" + tab_pseudo[0] + "', '" + tab_pseudo[1] + "'")

					if (tab_pseudo[0].lower() == ".défaut"):
						if (jdr_name == "défaut"):
							return tab_pseudo[1];
						default = tab_pseudo[1];
					if (tab_pseudo and tab_pseudo[0][0] == '.' and
						jdr_name.lower().find(remove_prefix(tab_pseudo[0].lower(), ".")) > 0):
						return tab_pseudo[1]
	return default

@client.event
async def on_voice_state_update(member, before, after):
	aff_log(time.strftime("\n%d/%m/%y %H:%M", now))
	if (member.voice):
		aff_log(member.name + " a agit dans le salon vocal " + after.channel.name)
		jdr_name = after.channel.category.name
		pseudo = await whats_your_name(member, jdr_name)
		await member.edit(nick=pseudo)
	return

@client.event
async def on_message(message):
	aff_log(time.strftime("\n%d/%m/%y %H:%M", now))
	aff_log(message.author.name + " a écrit dans le salon " + message.channel.name)
	if (message.channel.category):
		jdr_name = message.channel.category.name
		pseudo = await whats_your_name(message.author, jdr_name)
	else:	# peut être enlevé si le par défaut gène
		pseudo = await whats_your_name(message.author, "défaut")
	await message.author.edit(nick=pseudo)
	if message.content.casefold().startswith("ping") == True:
		await message.channel.send("Pong");
	if message.content.casefold().find("trahison") != -1:
		await message.channel.send("Disgrâce");


client.run(os.getenv("TOKEN"))
