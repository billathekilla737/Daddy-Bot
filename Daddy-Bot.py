#import Discord API
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time


#Discord Bot Token
#Read token from file
tokenFile = open("private.txt", "r")
token = tokenFile.read()
tokenFile.close()

#Create bot object
