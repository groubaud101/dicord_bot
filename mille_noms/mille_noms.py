import os
import discord
import time


from discord import Webhook

# pour avoir une instance de bot
from discord.ext import commands

# pour avoir la date sur les logs quand le bot réagit
from datetime import datetime

# pour avoir le TOKEN dans un fichier de config
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="mn")

load_dotenv(dotenv_path="config");

#client = discord.Client(intents=default_intents)

config_channel_id = 846436512811319296 
# config channel : les pseudos doivent être formatés comme suit
# sur plusieurs lignes ou plusieurs messages
#
# .<nom de la catégorie du jdr> : <pseudo>
#
# Les espaces de par et d'autres des 2 points sont importants, exemple :
# .Warhammer : Jean Edouard de la Haute

now = time.localtime(time.time())

@bot.event
async def on_ready():
	print("Le bot est pret")

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
	aff_log("jdr_name : " + jdr_name + "\n")
	config_channel = bot.get_channel(config_channel_id)
	default = member.name
	async for config_pseudo in config_channel.history():
		if (member == config_pseudo.author):
			source_names = config_pseudo.content.split("\n")
			for each_jdr in source_names:
				if (each_jdr.startswith(".") and each_jdr.find(" : ") > 1):
					tab_pseudo = each_jdr.split(" : ")
					aff_log("tab_pseudo : '" + tab_pseudo[0] + "', '" + tab_pseudo[1] + "'")

					if (tab_pseudo[0].lower() == ".défaut"):
						if (jdr_name == "défaut"):
							return tab_pseudo[1];
						default = tab_pseudo[1];
					if (tab_pseudo and tab_pseudo[0][0] == '.' and
						jdr_name.lower().find(remove_prefix(tab_pseudo[0].lower(), ".")) > 0):
						return tab_pseudo[1]
	return default

@bot.event
async def on_voice_state_update(member, before, after):
	aff_log(time.strftime("%d/%m/%y %H:%M", now))
	if (member.voice):
		aff_log(member.name + " a agit dans le salon vocal " + after.channel.name)
		jdr_name = after.channel.category.name
		pseudo = await whats_your_name(member, jdr_name)
		await member.edit(nick=pseudo)
	return

@bot.event
async def on_message(message):
	aff_log(time.strftime("\n%d/%m/%y %H:%M", now))
	aff_log(message.author.name + " a écrit dans le salon " + message.channel.name)
	if (message.channel.category):
		jdr_name = message.channel.category.name
		pseudo = await whats_your_name(message.author, jdr_name)
# Les deux lignes suivantes peuvent être enlevées si le par défaut gène
	#else:
	#	pseudo = await whats_your_name(message.author, "défaut")
# La ligne suivante doit etre une tab de moins si il y a le else
		await message.author.edit(nick=pseudo)
	if message.content.casefold().startswith("ping") == True:
		await message.channel.send("Pong");
	if message.content.casefold().find("trahison") != -1:
		await message.channel.send("Disgrâce");

# Si vous copier coller le code pour faitre votre propre bot, vous devez
# remplacer cette ligne par bot.run("le numéro de token de votre bot")
bot.run(os.getenv("TOKEN"))
