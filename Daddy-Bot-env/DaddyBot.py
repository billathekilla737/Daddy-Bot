from Assets.F1_Functions import *
from Assets.Melee_Functions import *
from Assets.pStar_Names import *
from discord import app_commands # type: ignore
from discord.ext import commands # type: ignore
from Assets.FlatFuckFriday import *
import datetime
import pytz
from tabulate import tabulate


###############Bot Description#####################
#The goal of this bot is to give a new users a nickname from a list of names from a text file.
#The bot will also give the user a role from a list of roles from a text file.

def run_discord_bot():
    ###########Initialize Bot####################################
    #scrape_race_info()                                          #
    token, URL = Parse_Private()                                #
    Scrap_Names()                                               #
    Scrap_Melee()                                               #
    scrape_race_info()
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
        devchannel = client.get_channel(1115817757267730533)
        sent = False
        try:
            synced = await tree.sync()
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)

        #Send Startup Message to Dev Channel if the system time is not between 4-5a.m. chicago time
        #####################################################################
        chi_tz = pytz.timezone('America/Chicago')
        correctednow = datetime.datetime.now(chi_tz)
        if correctednow.hour < 4 or correctednow.hour > 5:
            await devchannel.send("I had an unscheduled restart!!!")
            pass



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
                    await channel.send(f"{FreePracticeRole.mention} **{Event}** is in **{TimeDelta}!**")
                    PrevEvent = Event

                #Ping if the User has the Qualifying role
                elif "Qualifying" in Event or "Sprint" in Event:
                    QualifyingRole = discord.utils.get(client.guilds[0].roles, name="Qualifying")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    await channel.send(f"{QualifyingRole.mention} **{Event}** is in **{TimeDelta}!**")
                    PrevEvent = Event
                    
                #Ping if the User has the Grand Prix role
                elif ("Grand Prix Grand Prix" in Event):
                    GrandPrix = discord.utils.get(client.guilds[0].roles, name="Grand Prix")
                    #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                    PrevEvent = Event
                    Event = Event[:-10]
                    await channel.send(f"{GrandPrix.mention} **{Event}** is in **{TimeDelta}!** <a:max_nice:1117178831120371824>")
                    

            #Melee Reminder
            #################################################################
            try:
                shouldSendMeleeReminder = isMeleeTime()
            except Exception as e:
                print(f"{e}  Error in isMeleeTime()")
                shouldSendMeleeReminder = False
            
            if shouldSendMeleeReminder and PrevMeleeEvent != MeleeEvent:
                MeleeRole = discord.utils.get(client.guilds[0].roles, name="Melee")
                #Message = f"{role.mention} {Event} is in {TimeDelta}!"
                await meleechannel.send(f"{MeleeRole.mention} {MeleeEvent} is Today!")
                PrevMeleeEvent = MeleeEvent

            #Flat Fuck Friday Reminder
            ################################################################
            if isFlatFuckFriday() and sent != True:
                #IT'S FLAT FUCK FRIDAY! :FlatFuck:
                #Send a message in General that it's Flat Fuck Friday!
                message = "<:FlatFuck:1117199409478914128> It's Flat Fuck Friday You Fucking Losers! <:FlatFuck:1117199409478914128> \nhttps://youtu.be/SqfurZF4Xg4"
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



    #Slash Commands
    ##############################################################################################################################################
    #TODO Add locations to f1 commands
    
    @tree.command(name="freepractice", description="Tells you the next F1 free practice event <:f1_logo:1132150006988673034>")
    async def freepractice(interaction: discord.Interaction, practice_number: str):
        date, time = find_next_of_type("Free Practice", practice_number)
        if date and time != None:
            await interaction.response.send_message("The next F1 **Free Practice** " + practice_number + f" event is on **{date} at {time}**")
        else:
            await interaction.response.send_message(f"Free Practice, Not Found")

    @tree.command(name = "qualifying", description = "Tells you the next F1 qualifying event")
    async def qualifying(interaction: discord.Interaction):
        date, time = find_next_of_type("Qualifying", None)
        if date and time != None:
            await interaction.response.send_message(f"The next F1 **Qualifying** event is on **{date} at {time}** <:f1_logo:1132150006988673034>")
        # else:
        #     date, time = find_next_of_type("Sprint",None)
        #     await interaction.response.send_message(f"There is NO qualifying, SPRINT is on {date} at {time} <:f1_logo:1132150006988673034>")

    @tree.command(name = "sprint", description = "Tells you the next F1 sprint event")
    async def sprint(interaction: discord.Interaction):
        date, time = find_next_of_type("Sprint",None)
        if date and time != None:
            await interaction.response.send_message(f"The next F1 **Sprint** event is on **{date} at {time}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"There is **NO Sprint** this week. <:f1_logo:1132150006988673034>")
        # else:
        #     date, time = find_next_of_type("Qualifying",None)
        #     await interaction.response.send_message(f"There is NO sprint, QUALIFYING is on {date} at {time} <:f1_logo:1132150006988673034>")

    #TODO Add Sprint Shootout Command
    #TODO Will not grab the next event from upcoming week if it has already happended.
    @tree.command(name = "sprintshootout", description = "Tells you the next F1 sprint shootout event")
    async def sprintshootout(interaction: discord.Interaction):
        date, time = find_next_of_type("Sprint Shootout",None)
        if date and time != None:
            await interaction.response.send_message(f"The next F1 **Sprint Shootout** event is on **{date} at {time}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"There is **NO Sprint Shootout** this week. <:f1_logo:1132150006988673034>")
    
    @tree.command(name = "grandprix", description = "Tells you the next F1 Grand Prix event")
    async def grandprix(interaction: discord.Interaction):
        date, time = find_next_of_type("Grand Prix",None)
        await interaction.response.send_message(f"The next <:f1_logo:1132150006988673034> **Grand Prix** event is on **{date} at {time}** <a:max_nice:1117178831120371824>")

    @tree.command(name="help", description="Tells you the commands for the bot")
    async def help(interaction: discord.Interaction):
        # Define the table headers
        headers = ["Command", "Description"]

        # Define the table rows
        rows = [
            ["/week", "Tells you the next F1 events for the week"],
            ["/nextevent", "Tells you the next F1 Event"],
            ["/freepractice [Number]", "Tells you the next F1 free practice event"],
            ["/qualifying", "Tells you the next F1 qualifying event"],
            ["/sprintshootout", "Tells you the next F1 sprint shootout event"],
            ["/sprint", "Tells you the next F1 sprint event"],
            ["/grandprix", "Tells you the next F1 Grand Prix event"],
            ["/help", "Tells you the commands for the bot"]
        ]

        # Create the table
        table = tabulate(rows, headers=headers, tablefmt="pipe")

        # Send the table as a message
        await interaction.response.send_message(f"Here are the available commands:\n\n```{table}```")

    #Redundant Code needs to be cleaned up
    ##############################################################################################################################################
    @tree.command(name = "nextevent", description = "Tells you the next F1 Event <:f1_logo:1132150006988673034>")
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
            await interaction.response.send_message(f"The next F1 event is **{Event} on {fpdate} at {fptime}** <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")    

        elif "Qualifying" in Event:
            date, time = find_next_of_type("Qualifying", None)
            await interaction.response.send_message(f"The next F1 event is **{Event} on {date} at {time}** <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")
        

        elif "Sprint" in Event and "Sprint Shootout" not in Event:
            # Handle Sprint event
            date, time = find_next_of_type("Sprint", None)
            await interaction.response.send_message(f"The next F1 event is **{Event} on {date} at {time}** <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")
        elif "Sprint Shootout" in Event:
            # Handle Sprint Shootout event
            date, time = find_next_of_type("Sprint Shootout", None)
            await interaction.response.send_message(f"The next F1 event is **{Event} on {date} at {time}** <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")
        elif "Grand Prix" in Event:
            date, time = find_next_of_type("Grand Prix", None)
            await interaction.response.send_message(f"The next F1 event is **{Event} on {date} at {time}** <a:max_nice:1117178831120371824> \n T-minus {TimeDelta} until the next event!")
        
        else:
            await interaction.response.send_message(f"The next F1 event is the **{Event} in {TimeDelta}** <a:max_nice:1117178831120371824>")
    #############################################################################################################################################

    @tree.command(name = "week", description = "Tells you the next F1 events for the week <:f1_logo:1132150006988673034>")
    async def week(interaction: discord.Interaction):
        FreePractice1Date, FreePractice1Time    = find_next_of_type("Free Practice", "1")
        FreePractice2Date, FreePractice2Time    = find_next_of_type("Free Practice", "2")
        FreePractice3Date, FreePractice3Time    = find_next_of_type("Free Practice", "3")
        QualifyingDate, QualifyingTime          = find_next_of_type("Qualifying", None)
        SprintDate, SprintTime                  = find_next_of_type("Sprint", None)
        SprintShootoutDate, SprintShootoutTime  = find_next_of_type("Sprint Shootout", None)
        GrandPrixDate, GrandPrixTime            = find_next_of_type("Grand Prix", None)
        Next_Location                           = str(find_json_Next_Event_Location())
        Next_Location                           = Next_Location[:-4]

        print(FreePractice2Time)
        headers = ["Location", "Event", "Date", "Time"]
        #If it is not a sprint shootout weekend
        if FreePractice2Time == None:
            rows = [
                [Next_Location, "Free Practice 1", FreePractice1Date, FreePractice1Time],
                [Next_Location, "Qualifying", QualifyingDate, QualifyingTime],
                [Next_Location, "Sprint Shootout", SprintShootoutDate, SprintShootoutTime] if SprintShootoutDate else None,
                [Next_Location, "Sprint", SprintDate, SprintTime] if SprintDate else None,
                [Next_Location, "Grand Prix", GrandPrixDate, GrandPrixTime]
            ]
                
        #If it is a sprint shootout weekend
        elif FreePractice2Time != None:
            rows = [
                [Next_Location, "Free Practice 1", FreePractice1Date, FreePractice1Time],
                [Next_Location, "Free Practice 2", FreePractice2Date, FreePractice2Time],
                [Next_Location, "Free Practice 3", FreePractice3Date, FreePractice3Time],
                [Next_Location, "Qualifying", QualifyingDate, QualifyingTime],
                [Next_Location, "Sprint Shootout", SprintShootoutDate, SprintShootoutTime] if SprintShootoutDate else None,
                [Next_Location, "Sprint", SprintDate, SprintTime] if SprintDate else None,
                [Next_Location, "Grand Prix", GrandPrixDate, GrandPrixTime]
            ]


        rows = [row for row in rows if row is not None]
        table = tabulate(rows, headers=headers, tablefmt="pipe")
        await interaction.response.send_message(f"```{table}```")




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



