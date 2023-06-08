#F1 Bot Functionality

import sys
#Vivenv pathing issue. Hacky Fix.
#Zack's PC Path
sys.path.append(r'c:\users\zacha\appdata\local\programs\python\python310\lib\site-packages')

#Alex's Pc Path
#sys.path.append(r'c:\users\daric\appdata\local\programs\python\python310\lib\site-packages')

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import regex as re
import random
import json
import datetime
import asyncio

#Every Function needed for F1 Functionality
def find_closest_event(IsTimeCheck):
    #with open('Assets/TestRace.Json', 'r') as f:
    with open('Assets/F1Information.json', 'r') as f:
        events = json.load(f)
    now = datetime.datetime.now()
    closest_event = None
    closest_delta = None
    for event_name, event_data in events.items():
        for sub_event_name, sub_event_data in event_data.items():
            event_time = sub_event_data['time'].strip()
            if not event_time:
                continue
            event_date_str = sub_event_data['date'] + ' ' + event_time
            event_date_str = event_date_str.replace(event_date_str.split()[1], str(month_to_number(event_date_str.split()[1])))
            event_date_str = f'{event_date_str} {datetime.datetime.now().year}'
            event_date = datetime.datetime.strptime(event_date_str, '%d %m %H:%M:%S %Y')
            delta = event_date - now
            #print(f'Checking event {sub_event_name}: {event_date} (delta={delta})')

            if delta.total_seconds() >= 0 and (closest_delta is None or delta < closest_delta):
                closest_event = sub_event_name
                closest_delta = delta
    if closest_event is None:
        return None
    else:
        if IsTimeCheck == True:
            #Race Time Check Comes Here
            return str(closest_delta)
        else:
            closest_delta = str(closest_delta)
            #Write a formated string to place the words Hours, Minutes, and Seconds in the correct place.
            closest_delta = closest_delta.replace(':', ' Hours, ', 1)
            closest_delta = closest_delta.replace(':', ' Minutes, ', 1)
            closest_delta = closest_delta.replace('.', ' Seconds', 1)
            #Write regex to cut off all text after the seconds place
            closest_delta = re.sub(r'(\d+ Hours, \d+ Minutes, \d+ Seconds).*', r'\1', closest_delta)
            return closest_event, closest_delta

def month_to_number(month):
    month_abbr = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    return month_abbr[month]

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
    from bs4 import BeautifulSoup
    import json
    URL = 'https://f1calendar.com/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
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
            #if "Grand Prix Grand Prix" not in race_type:
            races[race_name][race_type] = {'date': race_date, 'time': race_time}
    with open('Assets/F1Information.json', 'w') as f1Info:
        json.dump(races, f1Info)

def IsRaceTime():
    #Checks if the Event is less than 30 minutes away
    closest_delta = find_closest_event(True)
    try:
        pattern = r'(\d+) days, (\d+):(\d+):'
        match = re.search(pattern, closest_delta)
        
        #if days exist set to match.group1 else set to None
        days = int(match.group(1))
        hours = int(match.group(2))
        minutes = int(match.group(3))
    except:
        pattern = r'(\d+):(\d+):'
        match = re.search(pattern, closest_delta)
        hours = int(match.group(1))
        minutes = int(match.group(2))
        days = None

    if days == None and hours == 0 and minutes <= 30:
        return True
    else:
        return False