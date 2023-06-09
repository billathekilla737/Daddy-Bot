from Assets.F1_Functions import *
from discord import app_commands
from Assets.Melee_Functions import *

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
    tree = discord.app_commands.CommandTree(client)            #
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
        await tree.sync(guild=discord.Object(id=632027077670862880))

        #   RECURRING TASKS (5 sec Loop)
        #####################################################################
        while True:
            shouldSendMessages = IsRaceTime()
            if shouldSendMessages and PrevEvent != Event:
                Event, TimeDelta = find_closest_event(None)
                #Ping the for every event
                if Event:
                    #No longer in use. Formally used to ping the user for every event
                    pass

                #Ping if the User has the Free Practice role
                if ("Free Practice" in Event):
                    FreePracticeRole = discord.utils.get(client.guilds[0].roles, name="Free Practice")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    await channel.send(f"{FreePracticeRole.mention} {Event} is in {TimeDelta}!")
                    PrevEvent = Event

                #Ping if the User has the Qualifying role
                if ("Qualifying" or "Sprint" in Event):
                    QualifyingRole = discord.utils.get(client.guilds[0].roles, name="Qualifying")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    await channel.send(f"{QualifyingRole.mention} {Event} is in {TimeDelta}!")
                    PrevEvent = Event

                #Ping if the User has the Grand Prix role
                if ("Grand Prix Grand Prix" in Event):
                    GrandPrix = discord.utils.get(client.guilds[0].roles, name="Grand Prix")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    await channel.send(f"{GrandPrix.mention} {Event} is in {TimeDelta}!")
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
    


            #Slash Commands
    ##############################################################################################################################################
    #Create a / command to tell the next "Qualifying" event
    @tree.command(name = "qualifying", description = "Tells you the next qualifying event")
    async def qualifying(interaction: discord.Interaction):
        find_next_of_type("Qualifying")
        await interaction.response.send_message(f"{find_next_of_type('Qualifying')}")
    
    #Create a / command to tell the next "Free Practice" event
    @tree.command(name = "freepractice", description = "Tells you the next free practice event")
    async def freepractice(interaction: discord.Interaction):
        find_next_of_type("Free Practice")
        await interaction.response.send_message(f"{find_next_of_type('Free Practice')}")

    #Create a / command to tell the next "Grand Prix" event
    @tree.command(name = "grandprix", description = "Tells you the next grand prix event")
    async def grandprix(interaction: discord.Interaction):
        find_next_of_type("Grand Prix")
        await interaction.response.send_message(f"{find_next_of_type('Grand Prix')}")

    #Create a / command to tell the next "Sprint" event
    @tree.command(name = "sprint", description = "Tells you the next sprint event", guild=discord.Object(id=632027077670862880))
    async def sprint(interaction: discord.Interaction):
        find_next_of_type("Sprint")
        await interaction.response.send_message(f"{find_next_of_type('Sprint')}")
    ##############################################################################################################################################

    





    client.run(token)


#Start the bot
#################################################################################################
                                                                                                #
                                                                                                #
run_discord_bot()                                                                               #
                                                                                                #
                                                                                                #
#################################################################################################

# Names, Dates = Scrap_Melee()
# for i in range(len(Names)):
#     print(f"{Names[i]}: {Dates[i]}")