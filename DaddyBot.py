#import Discord API

import sys
#Vivenv pathing issue. Hacky Fix.
sys.path.append(r'c:\users\zacha\appdata\local\programs\python\python310\lib\site-packages')
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import regex as re
import random



#TODO: Have the bot scrape https://f1calendar.com/ once every three days. Have it grab the Time of FP1,FP2,FP3, Qualifying, and Grand Prix.
#cont. Have the bot post the times in the f1 channel in the discord server, and @everyone with the f1 role 30min before the event starts.   

###############Bot Description#####################
#The goal of this bot is to give a new users a nickname from a list of names from a text file.
#The bot will also give the user a role from a list of roles from a text file.

def run_discord_bot():
    ###########Initialize Bot#######################
    token, URL = Parse_Private()                   #
    Scrap_Names()                                  #
    intents = discord.Intents.default()            #
    intents.message_content = True                 #
    intents.members = True                         #
    intents.presences = True                       #
    client = discord.Client(intents=intents)       #
    #Set the bot's status                          #
    nameList, roleList = Grab_Files()              #
    ################################################



    ###########Bot Events###########################################################################
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
        await client.change_presence(activity=discord.Game('with your mom'))

    @client.event
    async def on_member_join(member):
        #Change the user's nickname
        randomName = random.choice(nameList)
        await member.edit(nick=randomName)
        #Provide the user with a role
        await member.add_roles(discord.utils.get(member.guild.roles, name=roleList[2]))

    #TODO: Compare current time of system with time of Next F1 event. If the difference is less than 30min, @everyone with the f1 role.










    #Start the bot
    ####################
    client.run(token)





def Grab_Files():
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

    return nameList, roleList


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

def Scrape_F1Information():
    print("Scraping F1 Information. This will take a few seconds.")
    import requests
    import time
    from bs4 import BeautifulSoup
    f1File = open("Assets/F1Information.txt", "w")
    URL = 'https://f1calendar.com/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #TODO: Expand all hidden events with their times
    #TODO: Grab the times of FP1, FP2, FP3, Qualifying, and Grand Prix
    #TODO: Grab the Next Event
