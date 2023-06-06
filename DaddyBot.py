#import Discord API

import sys
#Vivenv pathing issue. Hacky Fix.
sys.path.append(r'c:\users\zacha\appdata\local\programs\python\python310\lib\site-packages')
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import regex as re
import random


#Discord Bot Token
#Read token from file
tokenFile = open("Assets\Private.txt", "r")
token = tokenFile.read()
tokenFile.close()

###############Bot Description#####################
#The goal of this bot is to give a new users a nickname from a list of names from a text file.
#The bot will also give the user a role from a list of roles from a text file.






def Parse_Private():
    tokenFile = open("Assets/Private.txt", "r")
    token = tokenFile.read()
    tokenFile.close()
    #Use Regex to grab the token and URL from the file '([^']*)'
    pattern = r"'(.*?)'"
    # Extract the values and store them in a list
    try:
        values = re.findall(pattern, token)
    except:
        print("Error: Private Information Not Found!")
    # Print the list
    token = values[0]
    URL = values[1]

    return token, URL

def run_discord_bot():
    global names, roles
    token, URL = Parse_Private()
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.presences = True
    client = discord.Client(intents=intents)
    

    #Preload the list of names and roles from the text files
    try:
        nameFile = open("Assets/Names.txt", "r")
        names = nameFile.read()
        nameList = names.splitlines()
        nameFile.close()
    except:
        print("Error: Names.txt not found!")
    #Grab the list of roles from the text file
    try:
        roleFile = open("Assets/Roles.txt", "r")
        roles = roleFile.read()
        roleList = roles.splitlines()
        roleFile.close()
    except:
        print("Error: Roles.txt not found!")
    
    



    #Called when a new user joins the server
    @client.event
    async def on_member_join(member):

        randomName = random.choice(nameList)
        await member.edit(nick=randomName)
       
        #Give the new member role[2] from the list of roles (NOT RANDOM)

        await member.add_roles(discord.utils.get(member.guild.roles, name="Average Dick Daddies"))
     
    
        
        #str(roleList[2]))
    print(roleList[2])
    client.run(token)   
    
    



def Scrap_Names():
    #If "Assets\Names.txt" does not exist, create it.
    try:
        nameFile = open("Assets/Names.txt", "r")
        nameFile.close()
    except:
        print("Scraping Names. This will take a few seconds.")
        import requests
        import time
        from bs4 import BeautifulSoup
        nameFile = open("Assets/Names.txt", "w")
        URL = 'https://www.pornhub.com/pornstars?gender=male&age=18-30'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        Names = soup.find_all('span', class_='pornStarName performerCardName')

        #TODO: Grab the names of the "Actors" from pages 2-10
        pagenum = 2
        while pagenum != 10:
            #Add a delay to be considerate to site
            time.sleep(.2)
            url = f"https://www.pornhub.com/pornstars?gender=male&age=18-30&page={pagenum}"
            pagenum = pagenum + 1
            reponse = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            Names = Names + soup.find_all('span', class_='pornStarName performerCardName')

        #Write the names to the file
        nameFile = open("Assets/Names.txt", "w")
        for i in range(len(Names)):
            nameFile.write(Names[i].text)
        nameFile.close()


Scrap_Names()
run_discord_bot()
