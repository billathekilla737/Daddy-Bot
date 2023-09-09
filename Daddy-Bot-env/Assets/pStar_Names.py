def Scrap_Names():
    #If "Assets\Names.txt" does not exist, create it.
    nameFile = open("Daddy-Bot-env/Assets/Names.txt", "r")
    print("Scraping Names. This will take a few seconds.")
    import requests
    import time
    from bs4 import BeautifulSoup
    URL = 'https://www.pornhub.com/pornstars?gender=male&age=18-30'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    Names = soup.find_all('span', class_='pornStarName performerCardName')
    pagenum = 2
    while pagenum != 10:
        #Add a delay to be considerate to site
        time.sleep(.2)
        url = f"https://www.pornhub.com/pornstars?gender=male&age=18-30&page={pagenum}"
        pagenum = pagenum + 1
        reponse = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        Names = Names + soup.find_all('span', class_='pornStarName performerCardName')

    print("Scraping Complete. Writing to file.")
    for i in range(len(Names)):
        print(Names[i].text)
        nameFile.write(Names[i].text)
    nameFile.close()