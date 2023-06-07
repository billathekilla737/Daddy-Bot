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


def twentyfourhr_to_twelvehr(time):
    # Check if the time is in the expected format
    if ':' not in time:
        return 'Invalid time format'
    # Split the time into hours and minutes
    time = time.split(":")
    # Check if the time has at least two elements
    if len(time) < 2:
        return 'Invalid time format'
    hours = time[0]
    minutes = time[1]
    # Convert the hours and minutes to integers
    try:
        hours = int(hours)
        minutes = int(minutes)
    except ValueError:
        return 'Invalid time format'
    # Check if the hours and minutes are valid
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return 'Invalid time format'
    # If the hours are greater than or equal to 12, subtract 12 from the hours and add PM to the end
    if hours >= 12:
        if hours > 12:
            hours = hours - 12
        hours = str(hours)
        time = hours + ":" + str(minutes).zfill(2) + " PM"
    # If the hours are less than 12, add AM to the end
    else:
        hours = str(hours)
        time = hours + ":" + str(minutes).zfill(2) + " AM"
    return time

def correct_for_timezone(time):
    from datetime import datetime, timedelta
    # Return an empty string if the time argument is empty
    if not time:
        return ''

    # Split the time string into hours and minutes if it contains a colon character
    if ':' in time:
        hours, minutes = time.split(':')
    else:
        # If the time string does not contain a colon character, assume that the minutes are 00
        hours = time
        minutes = '00'

    # Subtract 6 hours from the hours
    corrected_hours = int(hours) - 6

    # Add 24 to the corrected hours if they are less than 0
    if corrected_hours < 0:
        corrected_hours += 24

    # Combine the corrected hours and minutes into a datetime object
    corrected_time_obj = datetime(1900, 1, 1, corrected_hours, int(minutes))

    # Convert the corrected datetime object back to a string
    corrected_time = corrected_time_obj.strftime('%H:%M:%S')

    return corrected_time

def scrape_race_info():
    import requests
    import time
    import json
    from bs4 import BeautifulSoup
    URL = 'https://f1calendar.com/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    f1Info = open("Assets/F1Information.json", "w")
    race_tables = soup.select('tbody[id]')
    races = {}
    for race_table in race_tables:
        race_name = race_table.select_one('td span').text
        races[race_name] = {}
        race_rows = race_table.find_all('tr')
        for race_row in race_rows:
            race_type = race_row.select_one('td:nth-of-type(2)').text.strip()
            race_date = race_row.select_one('td:nth-of-type(3)').text.strip()
            race_time = race_row.select_one('td:nth-of-type(4)').text.strip()
            race_time = correct_for_timezone(race_time)
            print(race_type)
            if "Grand Prix Grand Prix" not in race_type:
                races[race_name][race_type] = {'date': race_date, 'time': race_time}
            else:
                print("Duplicate")
    print(races)
    f1Info.write(str(races))



    
scrape_race_info()
f1Info = open("Assets/F1Information.txt", "r")
f1Info = f1Info.read()