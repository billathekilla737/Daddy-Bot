# F1 Bot Functionality

import sys
from typing import List, Optional

from DaddyBot.data import GrandPrix


# Vivenv pathing issue. Hacky Fix.
# Zack's PC Path
sys.path.append(
    r"c:\users\zacha\appdata\local\programs\python\python310\lib\site-packages"
)


# Alex's Pc Path
# sys.path.append(r'c:\users\daric\appdata\local\programs\python\python310\lib\site-packages')

import discord
import re
import random
import json
import datetime
import asyncio
from pathlib import Path
from discord import Interaction
from discord import app_commands
from discord.ext import commands
from DaddyBot.data import RaceEvent, get_F1_events

data_dir = Path(__file__).parent.parent / "data"
__closest_set_flag: bool = False
__closest_event: Optional[RaceEvent] = None
__now: datetime.datetime = datetime.datetime.now()


# Every Function needed for F1 Functionality
def find_closest_event():
    # with open('Daddy-Bot-env/Assets/TestRace.Json', 'r') as f:
    now = datetime.datetime.now()
    closest_event = None
    closest_delta = datetime.timedelta(days=9999)
    if next_prix := find_next_prix():
        for event in next_prix.events:
            delta = event.time - now

            if delta.total_seconds() >= 0 and (delta < closest_delta):
                closest_event = event
            closest_delta = delta
        __closest_set_flag = True
    __closest_event = closest_event
    return __closest_event, closest_delta


def time_check():
    if not __closest_set_flag:
        find_closest_event()
    return None if __closest_event is None else (__now - __closest_event.time)




def find_next_of_type(event_type:str):
    next_prix = find_next_prix()
    if next_prix is None:
        return "Error: No Next Event Found!"
    
    

    supported_types = ["Free Practice".lower(), "Qualifying".lower(), "Sprint".lower(), "Grand Prix".lower()]
    if event_type.lower() not in supported_types:
        return "Error: Invalid Event Type"
    
    __now = datetime.datetime.now()
    for event in next_prix.events:
        if event_type.lower() in event.name.lower():
            if event.time > __now:
                return event
    else:
        return None, None

    # Clean up the readability of the date and time
    time = twentyfourhr_to_twelvehr(time)
    month = date[-3:]
    date = month + " " + date[:2]
    return date, time


def find_next_prix() -> GrandPrix | None:
    return next((prix for prix in get_F1_events() if prix.next), None)
    


def month_to_number(month):
    month_abbr = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    return month_abbr[month]


def Grab_Files():
    try:
        nameFile = open("Daddy-Bot-env/Assets/Names.txt", "r")
        names = nameFile.read()
        nameList = names.splitlines()
        nameFile.close()
    except:
        print("Error: Names.txt not found!")
    # Grab the list of roles from the text file
    try:
        roleFile = open("Daddy-Bot-env/Assets/Roles.txt", "r")
        roles = roleFile.read()
        roleList = roles.splitlines()
        roleFile.close()
    except:
        print("Error: Roles.txt not found!")

    return nameList, roleList


def Scrape_Names():
    # If "Assets\Names.txt" does not exist, create it.
    try:
        nameFile = open("Daddy-Bot-env/Assets/Names.txt", "r")
        nameFile.close()
    except:
        print("Scraping Names. This will take a few seconds.")
        import requests
        import time
        from bs4 import BeautifulSoup

        nameFile = open("Daddy-Bot-env/Assets/Names.txt", "w")
        URL = "https://www.pornhub.com/pornstars?gender=male&age=18-30"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        Names = soup.find_all("span", class_="pornStarName performerCardName")

        # TODO: Grab the names of the "Actors" from pages 2-10
        pagenum = 2
        while pagenum != 10:
            # Add a delay to be considerate to site
            time.sleep(0.2)
            url = f"https://www.pornhub.com/pornstars?gender=male&age=18-30&page={pagenum}"
            pagenum = pagenum + 1
            reponse = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            Names = Names + soup.find_all(
                "span", class_="pornStarName performerCardName"
            )

        # Write the names to the file
        nameFile = open("Daddy-Bot-env/Assets/Names.txt", "w")
        for i in range(len(Names)):
            nameFile.write(Names[i].text)
        nameFile.close()


def Parse_Private():
    tokenFile = open("Daddy-Bot-env/Assets/Private.txt", "r")
    token = tokenFile.read()
    tokenFile.close()
    # Use Regex to grab the token and URL from the file '([^']*)'
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
    if ":" not in time:
        return "Invalid time format"
    # Split the time into hours and minutes
    time = time.split(":")
    # Check if the time has at least two elements
    if len(time) < 2:
        return "Invalid time format"
    hours = time[0]
    minutes = time[1]
    # Convert the hours and minutes to integers
    try:
        hours = int(hours)
        minutes = int(minutes)
    except ValueError:
        return "Invalid time format"
    # Check if the hours and minutes are valid
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
        return "Invalid time format"
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
        return ""

    # Split the time string into hours and minutes if it contains a colon character
    if ":" in time:
        hours, minutes = time.split(":")
    else:
        # If the time string does not contain a colon character, assume that the minutes are 00
        hours = time
        minutes = "00"

    # Subtract 6 hours from the hours
    corrected_hours = int(hours) - 6

    # Add 24 to the corrected hours if they are less than 0
    if corrected_hours < 0:
        corrected_hours += 24

    # Combine the corrected hours and minutes into a datetime object
    corrected_time_obj = datetime(1900, 1, 1, corrected_hours, int(minutes))

    # Convert the corrected datetime object back to a string
    corrected_time = corrected_time_obj.strftime("%H:%M:%S")

    return corrected_time


def scrape_race_info():
    import requests
    from bs4 import BeautifulSoup
    import json

    URL = "https://f1calendar.com/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    race_tables = soup.select("tbody[id]")
    races = {}
    for race_table in race_tables:
        race_name = race_table.select_one("td span").text
        races[race_name] = {}
        race_rows = race_table.find_all("tr")
        for race_row in race_rows:
            race_type = race_row.select_one("td:nth-of-type(2)").text.strip()
            race_date = race_row.select_one("td:nth-of-type(3)").text.strip()
            race_time = race_row.select_one("td:nth-of-type(4)").text.strip()
            race_time = correct_for_timezone(race_time)
            # if "Grand Prix Grand Prix" not in race_type:
            races[race_name][race_type] = {"date": race_date, "time": race_time}
    with open("Daddy-Bot-env/Assets/F1Information.json", "w") as f1Info:
        json.dump(races, f1Info)


def IsRaceTime():
    # Checks if the Event is less than 30 minutes away
    closest_delta = find_closest_event(True)
    try:
        pattern = r"(\d+) days, (\d+):(\d+):"
        match = re.search(pattern, closest_delta)

        # if days exist set to match.group1 else set to None
        days = int(match.group(1))
        hours = int(match.group(2))
        minutes = int(match.group(3))
    except:
        pattern = r"(\d+):(\d+):"
        match = re.search(pattern, closest_delta)
        hours = int(match.group(1))
        minutes = int(match.group(2))
        days = None

    return days is None and hours == 0 and minutes <= 30


# intents = discord.Intents.all()
# client = discord.Client(command_prefix='/',intents=intents)
# tree = app_commands.CommandTree(client)


# Commands
# @tree.command(name="freepractice", description="Tells you the next F1 free practice event")
@commands.command(
    name="freepractice", description="Tells you the next F1 free practice event"
)
async def freepractice(interaction: discord.Interaction, practice_number: str):
    date, time = find_next_of_type("Free Practice")
    if date and time != None:
        await interaction.response.send_message(
            "The next F1 free practice "
            + practice_number
            + f" event is on {date} at {time}"
        )
    else:
        await interaction.response.send_message(f"Free Practice, Not Found")


# @tree.command(name = "qualifying", description = "Tells you the next F1 qualifying event")
async def qualifying(interaction: discord.Interaction):
    date, time = find_next_of_type("Qualifying", None)
    if date and time != None:
        await interaction.response.send_message(
            f"the next F1 qualifying event is on {date} at {time}"
        )
    else:
        date, time = find_next_of_type("Sprint", None)
        await interaction.response.send_message(
            f"There is NO qualifying, SPRINT is on {date} at {time}"
        )


# @tree.command(name = "sprint", description = "Tells you the next F1 sprint event")
async def sprint(interaction: discord.Interaction):
    date, time = find_next_of_type("Sprint", None)
    if date and time != None:
        await interaction.response.send_message(
            f"The next F1 sprint event is on {date} at {time}"
        )
    else:
        date, time = find_next_of_type("Qualifying", None)
        await interaction.response.send_message(
            f"There is NO sprint, QUALIFYING is on {date} at {time}"
        )


# @tree.command(name = "grandprix", description = "Tells you the next F1 Grand Prix event")
async def grandprix(interaction: discord.Interaction):
    date, time = find_next_of_type("Grand Prix", None)
    await interaction.response.send_message(
        f"The next F1 Grand Prix event is on {date} at {time}"
    )


# @tree.command(name = "week", description = "Tells you the next F1 events for the week")
async def week(interaction: discord.Interaction):
    FreePractice1Date, FreePractice1Time = find_next_of_type("Free Practice", "1")
    FreePractice2Date, FreePractice2Time = find_next_of_type("Free Practice", "2")
    FreePractice3Date, FreePractice3Time = find_next_of_type("Free Practice", "3")
    QualifyingDate, QualifyingTime = find_next_of_type("Qualifying", None)
    SprintDate, SprintTime = find_next_of_type("Sprint", None)
    GrandPrixDate, GrandPrixTime = find_next_of_type("Grand Prix", None)
    Next_Location = str(find_next_prix())
    Next_Location = Next_Location[:-4]
    if QualifyingDate and QualifyingTime != None:
        await interaction.response.send_message(
            "The next F1 Event is at "
            + Next_Location
            + f" dates and times are: \n\nFree Practice 1 on {FreePractice1Date} at {FreePractice1Time} \nFree Practice 2 on {FreePractice2Date} at {FreePractice2Time} \nFree Practice 3 on {FreePractice3Date} at {FreePractice3Time} \nQualifying on {QualifyingDate} at {QualifyingTime} \nGrand Prix on {GrandPrixDate} at {GrandPrixTime}"
        )
    else:
        await interaction.response.send_message(
            "The next F1 Event is at "
            + Next_Location
            + f" dates and times are: \n\nFree Practice 1 on {FreePractice1Date} at {FreePractice1Time} \nFree Practice 2 on {FreePractice2Date} at {FreePractice2Time} \nFree Practice 3 on {FreePractice3Date} at {FreePractice3Time} \nSprint on {SprintDate} at {SprintTime} \nGrand Prix on {GrandPrixDate} at {GrandPrixTime}"
        )


async def setup(bot):
    bot.add_command(freepractice)
if __name__=="__main__":
    print(find_next_prix())
