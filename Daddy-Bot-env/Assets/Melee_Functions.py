from Assets.F1_Functions import month_to_number
import json
import pytz

def Scrap_Melee():
    
    print("Scraping Melee Data. This will take a few seconds.")
    import requests
    import time
    from bs4 import BeautifulSoup
    import re

    Meleejson = {}
    URL = 'https://meleemajors.com/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
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



   

    #Get the current month
    chi_tz = pytz.timezone('America/Chicago')
    correctednow = datetime.datetime.now(chi_tz)
    current_sys_month = correctednow.strftime("%m")
    #if current month has a 0 in front, remove it
    if current_sys_month[0] == "0":
        current_sys_month = current_sys_month[1:]
    #Get the current day
    current_sys_day = correctednow.strftime("%d")
    #if current day has a 0 in front, remove it
    if current_sys_day[0] == "0":
        current_sys_day = current_sys_day[1:]
    

    #Will only work "One time deep". Could be made into a loop.
    if NextMonth[0] == current_sys_month and int(current_sys_day) > int(EndDate):
        NextMonth = list(Meleejson.values())[1]["Month"]
        StartDate = list(Meleejson.values())[1]["Start Date"]
        EndDate = list(Meleejson.values())[1]["End Date"]
        NextMajor = list(Meleejson.keys())[1]
    return NextMajor, NextMonth, StartDate, EndDate

def isMeleeTime():
    #Find the timedelta from now sys time to closed event time starting day. If less than 1 day, return true
    from datetime import datetime
    import time
    MajorName, Month, StartDate, EndDate = find_Next_Major()
    #Use Datetime to get the current month
    chi_tz = pytz.timezone('America/Chicago')
    correctednow = datetime.now(chi_tz)
    current_sys_month = correctednow.strftime("%m")
    current_sys_day = correctednow.strftime("%d")
    #if current month has a 0 in front, remove it 
    if current_sys_month[0] == "0":
        current_sys_month = current_sys_month[1:]
        #remove and spaces
    current_sys_month = current_sys_month.replace(" ", "")
    current_sys_day = current_sys_day.replace(" ", "")

    #print(f"Current Month: {current_sys_month} Current Day: {current_sys_day} Next Major Month: {Month} Next Major Start Date: {StartDate} Next Major End Date: {EndDate}")
    
    #If the current month is the same as the month of the next major
    if current_sys_month == Month:
        #If the current day is greater than or equal to the start date
        if int(current_sys_day) >= int(StartDate):
            #If the current day is less than or equal to the end date
            if int(current_sys_day) <= int(EndDate):
                return True
    return False

    

#Super Jank to add these back in retoactively
def monthNum_to_full_Name(monthNum):
    monthNum = int(monthNum)
    if monthNum == 1:
        return "January"
    elif monthNum == 2:
        return "February"
    elif monthNum == 3:
        return "March"
    elif monthNum == 4:
        return "April"
    elif monthNum == 5:
        return "May"
    elif monthNum == 6:
        return "June"
    elif monthNum == 7:
        return "July"
    elif monthNum == 8:
        return "August"
    elif monthNum == 9:
        return "September"
    elif monthNum == 10:
        return "October"
    elif monthNum == 11:
        return "November"
    elif monthNum == 12:
        return "December"
    else:
        return "Error"
    
#Super Jank to add these back in retoactively
def dateReadabilty(date):
    #If the date is 1, 21, or 31, add st to the end
    if date == "1" or date == "21" or date == "31":
        return date + "st"
    #If the date is 2 or 22, add nd to the end
    elif date == "2" or date == "22":
        return date + "nd"
    #If the date is 3 or 23, add rd to the end
    elif date == "3" or date == "23":
        return date + "rd"
    #Else, add th to the end
    else:
        return date + "th"