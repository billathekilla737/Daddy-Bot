from Assets.F1_Functions import *



###############Bot Description#####################
#The goal of this bot is to give a new users a nickname from a list of names from a text file.
#The bot will also give the user a role from a list of roles from a text file.

def run_discord_bot():
    ###########Initialize Bot###########################
    scrape_race_info()                                 #
    token, URL = Parse_Private()                       #
    Scrap_Names()                                      #
    intents = discord.Intents.default()                #
    intents.message_content = True                     #
    intents.members = True                             #
    intents.presences = True                           #
    client = discord.Client(intents=intents)           #
    #Set the bot's status                              #
    nameList, roleList = Grab_Files()                  #
    ####################################################



    #################################-Bot Events-########################################
    async def on_ready():
        #Variable Initialization
        #####################################################################
        print('We have logged in as {0.user}'.format(client))
        await client.change_presence(activity=discord.Game('with your mom'))
        PrevEvent = "" 
        Event, TimeDelta = find_closest_event(False) 
        channel = client.get_channel(907764974099787797)

        #   RECURRING TASKS (5 sec Loop)
        #####################################################################
        while True:
            shouldSendMessages = IsRaceTime()
            if shouldSendMessages and PrevEvent != Event:
                Event, TimeDelta = find_closest_event(None)
                if "Free Practice" not in Event:
                    role = discord.utils.get(client.guilds[0].roles, name="F1")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    await channel.send(f"{role.mention} {Event} is in {TimeDelta}!")
                    PrevEvent = Event
            await asyncio.sleep(5)

    @client.event
    async def on_member_join(member):
        #Change the user's nickname
        randomName = random.choice(nameList)
        await member.edit(nick=randomName)
        #Provide the user with a role
        await member.add_roles(discord.utils.get(member.guild.roles, name=roleList[2]))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$f1'):
            NextEvent, TimeDelta = find_closest_event(None)
            #Send message with time and event to the user as a reply
            await message.channel.send(f"{NextEvent} is in {TimeDelta}!")

    client.run(token)


#Start the bot
#################################################################################################
                                                                                                #
                                                                                                #
run_discord_bot()                                                                               #
                                                                                                #
                                                                                                #
#################################################################################################


#with open('Assets/F1Information.json') as f:
#    data = json.load(f)
#
#eventType = ""
#time = data["Brazilian Grand Prix"]["Brazilian Grand Prix" + eventType]["time"]
#date = data["Brazilian Grand Prix"]["Brazilian Grand Prix" + eventType]["date"]

# TODO
# " Free Practice 1"
# " Free Practice 2"
# " Free Practice 3"
# " Qualifying"
# " Sprint Shootout"
# " Sprint"
# ""
# "Brazilian Grand Prix Free Practice 1" check against above
# check string from find_closest_event

