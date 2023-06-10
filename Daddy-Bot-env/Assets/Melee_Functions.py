def Scrap_Melee():
    import json
    print("Scraping Melee Data. This will take a few seconds.")
    import requests
    import time
    from bs4 import BeautifulSoup

    Meleejson = {}
    URL = 'https://meleemajors.com/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    Names = soup.find_all('span', class_='pornStarName performerCardName')

    #Grab the info for every class card with h4
    Dates = [event.text for event in soup.find_all('h4')]
    #Grab the Event Names
    Names = [name.text for name in soup.find_all('h2')]
    #Remove the first two elements in Names
    Names = Names[2:]


    #Write the data to a json file with the event name as the key and the date as the value
    for i in range(len(Names)):
        #Split the date into two seperate values strings the start and end date
        Dates[i] = Dates[i].split(" - ")
        #Store the start date as a variable
        StartDate = Dates[i][0]
        #Store the end date as a variable
        EndDate = Dates[i][1]
        #Store the event name as a variable
        EventName = Names[i]
        #Store the event name as a key and the start and end date as the value
        Meleejson[EventName] = [StartDate, EndDate]
        
        


    with open('Daddy-Bot-env/Assets/Melee.json', 'w') as outfile:
        json.dump(Meleejson, outfile)
        print("Scraping Complete")
    return Names, Dates