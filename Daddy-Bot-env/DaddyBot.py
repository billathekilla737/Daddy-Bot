from Assets.F1_Functions import *
from Assets.Melee_Functions import *
from discord import app_commands # type: ignore
from discord.ext import commands # type: ignore
from Assets.FlatFuckFriday import *


###############Bot Description#####################
#The goal of this bot is to give a new users a nickname from a list of names from a text file.
#The bot will also give the user a role from a list of roles from a text file.

def run_discord_bot():
    ###########Initialize Bot####################################
    scrape_race_info()                                          #
    token, URL = Parse_Private()                                #
    Scrap_Names()                                               #
    Scrap_Melee()                                               #
    intents = discord.Intents.all()                             #
    global sent                                                 #
                                                                #
                                                                #
    client = discord.Client(command_prefix='/',intents=intents) #
    #Set the bot's status                                       #
    tree = app_commands.CommandTree(client)                     #
    #bot = commands.Bot(command_prefix='/', intents=intents)    #
    nameList, roleList = Grab_Files()                           #
    #############################################################
    
    #################################-Bot Events-########################################
    @client.event
    async def on_ready():
        #Variable Initialization
        #####################################################################
        print('We have logged in as {0.user}'.format(client))
        await client.change_presence(activity=discord.Game('with your mom'))
        PrevEvent = "" 
        Event, TimeDelta = find_closest_event(False) # type: ignore
        MeleeEvent, *_ = find_Next_Major()
        PrevMeleeEvent = ""
        channel = client.get_channel(907764974099787797)
        #meleechannel = client.get_channel(1117158502989844600)
        meleechannel = client.get_channel(1117158502989844600)
        sent = False
        try:
            synced = await tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)

        #Reaction Role Setup
        #####################################################################
        # reactText = ("React to this message to get the Melee role!")
        # Moji = await meleechannel.send(reactText)
        # await Moji.add_reaction('🥊')

        #   RECURRING TASKS (5 sec Loop)
        #####################################################################
        while True:
            #F1 Race Reminders
            #################################################################
            shouldSendF1Reminder = IsRaceTime()
            Event, TimeDelta = find_closest_event(False) # type: ignore
            if shouldSendF1Reminder and PrevEvent != Event:
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
                elif "Qualifying" in Event or "Sprint" in Event:
                    QualifyingRole = discord.utils.get(client.guilds[0].roles, name="Qualifying")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    await channel.send(f"{QualifyingRole.mention} {Event} is in {TimeDelta}!")
                    PrevEvent = Event
                    
                #Ping if the User has the Grand Prix role
                elif ("Grand Prix Grand Prix" in Event):
                    GrandPrix = discord.utils.get(client.guilds[0].roles, name="Grand Prix")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    PrevEvent = Event
                    Event = Event[:-10]
                    await channel.send(f"{GrandPrix.mention} {Event} is in {TimeDelta}! <a:max_nice:1117178831120371824>")
                    

            #Melee Reminder
            #################################################################
            shouldSendMeleeReminder = isMeleeTime()
            if shouldSendMeleeReminder and PrevMeleeEvent != MeleeEvent:
                MeleeRole = discord.utils.get(client.guilds[0].roles, name="Melee")
                #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                await meleechannel.send(f"{MeleeRole.mention} {MeleeEvent} is tomorrow!")
                PrevMeleeEvent = MeleeEvent
                        #Flat Fuck Friday Reminder
            ################################################################
            if isFlatFuckFriday() and sent != True:
                #IT'S FLAT FUCK FRIDAY! :FlatFuck:
                #Send a message in General that it's Flat Fuck Friday!
                message = "<:FlatFuck:1117199409478914128> It's Flat Fuck Friday You Fucking Losers! <:FlatFuck:1117199409478914128> \nhttps://youtu.be/A5U8ypHq3BU"
                GeneralChannel = client.get_channel(632027078371573775)
                await GeneralChannel.send(message)
                sent = True
                asyncio.create_task(reset_sent())
            await asyncio.sleep(45)
        

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
        if message.content.startswith('$test'):
            pass
            #Deactivated for now
            #NextEvent, TimeDelta = find_closest_event(None)
            #await message.channel.send(f"{NextEvent} is in {TimeDelta}!")
            await message.channel.send(" is in timeeeeee! <:LewisDab:844441514557440040>")
    


    #Slash Commands
    ##############################################################################################################################################
    @tree.command(name="freepractice", description="Tells you the next F1 free practice event")
    async def freepractice(interaction: discord.Interaction, practice_number: str):
        date, time = find_next_of_type("Free Practice", practice_number)
        if date and time != None:
            await interaction.response.send_message("The next F1 free practice " + practice_number + f" event is on {date} at {time}")
        else:
            await interaction.response.send_message(f"Free Practice, Not Found")

    @tree.command(name = "qualifying", description = "Tells you the next F1 qualifying event")
    async def qualifying(interaction: discord.Interaction):
        date, time = find_next_of_type("Qualifying", None)
        if date and time != None:
            await interaction.response.send_message(f"The next F1 qualifying event is on {date} at {time} <:Alex_SUSbon:1117179093562175650>")
        else:
            date, time = find_next_of_type("Sprint",None)
            await interaction.response.send_message(f"There is NO qualifying, SPRINT is on {date} at {time} <:Alex_SUSbon:1117179093562175650>")

    @tree.command(name = "sprint", description = "Tells you the next F1 sprint event")
    async def sprint(interaction: discord.Interaction):
        date, time = find_next_of_type("Sprint",None)
        if date and time != None:
            await interaction.response.send_message(f"The next F1 sprint event is on {date} at {time} <:Alex_SUSbon:1117179093562175650>")
        else:
            date, time = find_next_of_type("Qualifying",None)
            await interaction.response.send_message(f"There is NO sprint, QUALIFYING is on {date} at {time} <:Alex_SUSbon:1117179093562175650>")

    @tree.command(name = "grandprix", description = "Tells you the next F1 Grand Prix event")
    async def grandprix(interaction: discord.Interaction):
        date, time = find_next_of_type("Grand Prix",None)
        await interaction.response.send_message(f"The next F1 Grand Prix event is on {date} at {time} <a:max_nice:1117178831120371824>")


    @tree.command(name = "nextevent", description = "Tells you the next F1 Event")
    async def nextevent(interaction: discord.Interaction):
        Event, TimeDelta = find_closest_event(False)
        fpdate, fptime = None, None
        
        if "Free Practice" in Event:
            date, time = find_next_of_type("Free Practice", "1")
            if date:
                fpdate, fptime = date, time
            else:
                date, time = find_next_of_type("Free Practice", "2")
                if date:
                    fpdate, fptime = date, time
                else:
                    date, time = find_next_of_type("Free Practice", "3")
                    if date:
                        fpdate, fptime = date, time
            await interaction.response.send_message(f"The next F1 event is {Event} on {fpdate} at {fptime} <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")    

        elif "Qualifying" in Event or "Sprint" in Event:
            date, time = find_next_of_type("Qualifying", None)
            await interaction.response.send_message(f"The next F1 event is {Event} on {date} at {time} <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")
        
        elif "Grand Prix" in Event:
            date, time = find_next_of_type("Grand Prix", None)
            await interaction.response.send_message(f"The next F1 event is {Event} on {date} at {time} <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")
        
        else:
            await interaction.response.send_message(f"The next F1 event is the {Event} in {TimeDelta} <a:max_nice:1117178831120371824>")
    

    @tree.command(name = "week", description = "Tells you the next F1 events for the week")
    async def week(interaction: discord.Interaction):
        FreePractice1Date, FreePractice1Time = find_next_of_type("Free Practice", "1")
        FreePractice2Date, FreePractice2Time = find_next_of_type("Free Practice", "2")
        FreePractice3Date, FreePractice3Time = find_next_of_type("Free Practice", "3")
        QualifyingDate, QualifyingTime = find_next_of_type("Qualifying", None)
        SprintDate, SprintTime = find_next_of_type("Sprint", None)
        GrandPrixDate, GrandPrixTime = find_next_of_type("Grand Prix", None)
        Next_Location = str(find_json_Next_Event_Location())
        Next_Location = Next_Location[:-4]
        if QualifyingDate and QualifyingTime != None:
            await interaction.response.send_message('The next F1 Event is the' + Next_Location + f' dates and times are: \n\nFree Practice 1 on {FreePractice1Date} at {FreePractice1Time} \nFree Practice 2 on {FreePractice2Date} at {FreePractice2Time} \nFree Practice 3 on {FreePractice3Date} at {FreePractice3Time} \nQualifying on {QualifyingDate} at {QualifyingTime} \nGrand Prix on {GrandPrixDate} at {GrandPrixTime}')
        else:
            await interaction.response.send_message('The next F1 Event is the ' + Next_Location + f' dates and times are: \n\nFree Practice 1 on {FreePractice1Date} at {FreePractice1Time} \nFree Practice 2 on {FreePractice2Date} at {FreePractice2Time} \nFree Practice 3 on {FreePractice3Date} at {FreePractice3Time} \nSprint on {SprintDate} at {SprintTime} \nGrand Prix on {GrandPrixDate} at {GrandPrixTime}')
    
    @tree.command(name = "nextmeleemajor", description = "Tells you the next Melee Major Event is")
    async def meleemajor(interaction: discord.Interaction):
        NextMajor, Month, Start, End = find_Next_Major()
        await interaction.response.send_message(f"The next Melee Major is {NextMajor} in {monthNum_to_full_Name(Month)} from {dateReadabilty(Start)} to {dateReadabilty(End)}")
    
    #Reaction Roles
    ##############################################################################################################################################
    @client.event
    async def on_raw_reaction_add(payload):
        meleechannel = client.get_channel(1117158502989844600)
        if payload.emoji.name == "🥊" and payload.message_id == 1119503042144911440 and payload.channel_id == meleechannel.id:
            guild = await client.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            role = discord.utils.get(guild.roles, name="Melee")
            await member.add_roles(role)

    @client.event
    async def on_raw_reaction_remove(payload):
        meleechannel = client.get_channel(1117158502989844600)
        if payload.emoji.name == "🥊" and payload.message_id == 1119503042144911440 and payload.channel_id == meleechannel.id:
            guild = await client.fetch_guild(payload.guild_id)
            member = await guild.fetch_member(payload.user_id)
            role = discord.utils.get(guild.roles, name="Melee")
            await member.remove_roles(role)
    #Misc.
    ##############################################################################################################################################
    async def reset_sent():
        await asyncio.sleep(24 * 60 * 60) # Wait for 24 hours
        global sent
        sent = False
        print("Reset for FFF sent")
        
    
    ####Initilize the bot###
                           #
    client.run(token)      #
                           #
    ########################

#Start the bot
#################################################################################################
                                                                                                #
                                                                                                #
run_discord_bot()                                                                               #
                                                                                                #
                                                                                                #
#################################################################################################
