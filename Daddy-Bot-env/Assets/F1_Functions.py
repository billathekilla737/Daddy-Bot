#F1 Bot Functionality

import sys
#Vivenv pathing issue. Hacky Fix.
#Zack's PC Path
sys.path.append(r'c:\users\zacha\appdata\local\programs\python\python310\lib\site-packages')

#Alex's Pc Path
#sys.path.append(r'c:\users\daric\appdata\local\programs\python\python310\lib\site-packages')

import discord
import regex as re
import random
import json
import datetime
import asyncio
from discord import Interaction
import pytz
from datetime import datetime, timedelta
url = 'https://f1calendar.com/'
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
convert_to_12hr = lambda time_str: datetime.strptime(time_str, '%H:%M').strftime('%I:%M %p')



def scrape_f1_races(url):
    races = {}
    #convert_to_12hr = lambda time_str: datetime.strptime(time_str, '%H:%M').strftime('%I:%M %p')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the tbody element by ID, assuming each race's details are enclosed within a tbody with a unique ID
            race_details = soup.find_all('tbody', class_='text-white')
            for detail in race_details:
                # Extract the race title from the th element
                race_title = detail.find('th', id=lambda x: x and x.endswith('-header')).text.strip()
                # Initialize the race detail list
                races[race_title] = []
                # Extract all related event rows within the tbody
                event_rows = detail.find_all('tr')[1:]  # Skip the first row as it's the header
                for row in event_rows:
                    event_type = row.find_all('td')[1].text.strip()
                    date = row.find('td', headers=lambda x: x and x.endswith('date_header')).text.strip()
                    time = row.find('td', headers=lambda x: x and x.endswith('time_header')).find('div').text.strip()
                    Biscet_Africa = datetime.strptime(time, '%H:%M').replace(tzinfo=pytz.timezone('Africa/Abidjan'))
                    time_chicago = (Biscet_Africa.astimezone(pytz.timezone('America/Chicago')) - timedelta(minutes=25)).strftime('%H:%M')


                    #Decided not to use. Leaving if I want in the future.
                        #correctedTime = convert_to_12hr(time_chicago)
                    races[race_title].append({
                        "event_type": event_type,
                        "date": date,
                        "time": time_chicago
                    })
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)

    races_json = json.dumps(races, indent=4)
    with open('Daddy-Bot-env/Assets/F1Information.json', 'w') as file:
        file.write(races_json)
    return races_json

def find_next_event(races_json):
    # Convert current time to America/Chicago timezone
    current_time_chicago = datetime.now(pytz.timezone('America/Chicago'))
    
    try:
        with open(races_json, 'r') as file:
            races_json = json.load(file)
        # Now races_json is a dictionary, and you can use the previous logic here
        # Your logic to find the next event...
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")

    closest_event = None
    closest_time_diff = None

    for race_title, events in races_json.items():
        for event in events:
            # Assuming the year is the current year; adjust if necessary
            event_date_str = event["date"] + " " + str(current_time_chicago.year)
            event_datetime_str = f"{event_date_str} {event['time']}"
            
            # Convert event date and time to datetime object in America/Chicago timezone
            try:
                event_datetime = datetime.strptime(event_datetime_str, '%d %b %Y %H:%M')
                event_datetime = pytz.timezone('America/Chicago').localize(event_datetime)
            except ValueError:
                # Handle the case where date parsing fails
                print(f"Failed to parse date/time for event: {event['event_type']}")
                continue
            
            # Calculate time difference from now, if it's in the future
            if event_datetime > current_time_chicago:
                time_diff = event_datetime - current_time_chicago
                if closest_time_diff is None or time_diff < closest_time_diff:
                    closest_event = event
                    closest_time_diff = time_diff

    return closest_event

#TODO; For some reason this is 6hr off from the actual time. I.E. 1:30pm is 7:30am
def get_timedelta_to_next_event(races_json):
    # Assuming find_next_event() returns a dictionary with 'date' and 'time' keys
    next_event = find_next_event(races_json)
    
    if not next_event:
        return "No next event found."

    # Determine the current year and the year for the event
    current_time_chicago = datetime.now(pytz.timezone('America/Chicago'))
    current_year = current_time_chicago.year
    next_year = current_year + 1

    # First, try parsing the date as if the event is in the current year
    datetime_str = f"{next_event['date']} {next_event['time']} {current_year}"
    event_datetime = datetime.strptime(datetime_str, '%d %b %H:%M %Y').replace(tzinfo=pytz.timezone('America/Chicago'))

    # If the event datetime is in the past, it means the event is in the next year
    if event_datetime < current_time_chicago:
        datetime_str = f"{next_event['date']} {next_event['time']} {next_year}"
        event_datetime = datetime.strptime(datetime_str, '%d %b %H:%M %Y').replace(tzinfo=pytz.timezone('America/Chicago'))

    # Calculate the timedelta
    delta = event_datetime - current_time_chicago
    
    # Include days in the timedelta calculation
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format the timedelta to include days, hours, and minutes
    return days, hours, minutes


#TODO: Make this function try Except for when they ask for an event that doesn't exist. I.E. Sprint
def find_next_event_by_type(json_file_path, event_type_keyword):
    # Load JSON data from the file
    with open(json_file_path, 'r') as file:
        races_json = json.load(file)

    # Convert current time to America/Chicago timezone
    current_time_chicago = datetime.now(pytz.timezone('America/Chicago'))
    
    closest_event = None
    closest_time_diff = timedelta.max

    for race_title, events in races_json.items():
        for event in events:
            # Check if the event type keyword is part of the event type string
            if event_type_keyword in event["event_type"]:
                # Correct the datetime format to match the 24-hour format without AM/PM
                event_datetime_str = f"{event['date']} {event['time']} 2024"  # Adjust the year as necessary
                event_datetime = datetime.strptime(event_datetime_str, '%d %b %H:%M %Y')
                event_datetime = pytz.timezone('America/Chicago').localize(event_datetime)

                time_diff = event_datetime - current_time_chicago
                # Check if this event is closer to the current time than previous ones and is in the future
                if 0 < time_diff.total_seconds() < closest_time_diff.total_seconds():
                    closest_event = event
                    closest_time_diff = time_diff
    
    return closest_event

def IsRaceTime(races_json):
    days, hours, minutes = get_timedelta_to_next_event(races_json)
    if days == 0 and hours == 0 and minutes <= 30:
        return True
    else:
        return False


#Testing
#################################################################################################
#...
#...
#...
#Testing the Scrape Function
###############################################################
# Example usage
#races = scrape_f1_races(url)

#Testing the Find Next Event Function
###############################################################
#next_event = find_next_event('Daddy-Bot-env/Assets/F1Information.json')
#print(next_event)
#print('Next Event is: ' + next_event['event_type'] + ' on ' + next_event['date'] + ' at ' + convert_to_12hr(next_event['time']) + ' ... America/Chicago')

# Testing the Countdown to Next Event Function
#timedelta_to_next_event = get_timedelta_to_next_event('Daddy-Bot-env/Assets/F1Information.json')
#print(timedelta_to_next_event)

# #Testing the Find Next Event by Type Function
# ###############################################################
#event_type = "Free Practice 2"
#next_event = find_next_event_by_type('Daddy-Bot-env/Assets/F1Information.json', event_type)
#print('Next Event is: ' + next_event['event_type'] + ' on ' + next_event['date'] + ' at ' + convert_to_12hr(next_event['time']) + ' ... America/Chicago')
    
#Testing IsRaceTime Function
###############################################################
#...
    