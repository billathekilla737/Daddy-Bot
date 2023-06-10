from Assets.F1_Functions import month_to_number
import json
def Scrap_Melee():
    
    print("Scraping Melee Data. This will take a few seconds.")
    import requests
    import time
    from bs4 import BeautifulSoup
    import re

    Meleejson = {}
    URL = 'https://meleemajors.com/'
    page = requests.get(URL)
    Names = [name.text for name in soup.find_all('h2')]
    #Remove the first two elements in Names
    Names = Names[2:]

    Dates = [date.text for date in soup.find_all('h4')]
    Dates = [re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date) for date in Dates]

    Months = [date[:3] for date in Dates]
    Months = [month_to_number(month) for month in Months]
    Months = [str(month) for month in Months]
    
    Dates = [re.sub(r'[a-zA-Z]', r'', date) for date in Dates]
    Dates = [date.replace(" ", "") for date in Dates]
    Dates = [date.split("-") for date in Dates]
    StartDate = [date[0] for date in Dates]
    EndDate = [date[1] for date in Dates]

    for i in range(len(Names)):
        #Give each name a key
        Meleejson[Names[i]] = {}
        #Give each key a value
        Meleejson[Names[i]]["Month"] = Months[i]
        Meleejson[Names[i]]["Start Date"] = StartDate[i]
        Meleejson[Names[i]]["End Date"] = EndDate[i]
        
    
    #Write the json file
    with open('Daddy-Bot-env/Assets/Melee.json', 'w') as json_file:
        json.dump(Meleejson, json_file)

    return Names, Months, StartDate, EndDate

def find_Next_Major():
    with open('Daddy-Bot-env/Assets/Melee.json') as json_file:
        Meleejson = json.load(json_file)
    import datetime
    import time

    #Will be the first major in the json file
    NextMajor = list(Meleejson.keys())[0]
    #Will be the first date in the json file
    NextMonth = list(Meleejson.values())[0]["Month"]
    StartDate = list(Meleejson.values())[0]["Start Date"]
    EndDate = list(Meleejson.values())[0]["End Date"]

    return NextMajor, NextMonth, StartDate, EndDate

def isMeleeTime():
    #Find the timedelta from now sys time to closed event time starting day. If less than 1 day, return true
    from datetime import datetime
    import time
    MajorName, Month, StartDate, EndDate = find_Next_Major()
    #Use Datetime to get the current month
    now = datetime.now()
    current_sys_month = now.strftime("%m")
    current_sys_day = now.strftime("%d")
    #if current month has a 0 in front, remove it 
    if current_sys_month[0] == "0":
        current_sys_month = current_sys_month[1:]
        #remove and spaces
    current_sys_month = current_sys_month.replace(" ", "")
    current_sys_day = current_sys_day.replace(" ", "")


    #If the current month is the same as the month of the next major
    if current_sys_month == Month:
        #If the current day is greater than or equal to the start date
        if int(current_sys_day) >= int(StartDate):
            #If the current day is less than or equal to the end date
            if int(current_sys_day) <= int(EndDate):
                return True
    return False

#Super Jank but it works, and I'm feeling lazy. Should have never been converted to #.
def abv_to_full_month(month):
    if month == "Jan":
        return "January"
    elif month == "Feb":
        return "February"
    elif month == "Mar":
        return "March"
    elif month == "Apr":
        return "April"
    elif month == "May":
        return "May"
    elif month == "Jun":
        return "June"
    elif month == "Jul":
        return "July"
    elif month == "Aug":
        return "August"
    elif month == "Sep":
        return "September"
    elif month == "Oct":
        return "October"
    elif month == "Nov":
        return "November"
    elif month == "Dec":
        return "December"
    else:
        return "Error"

    


    