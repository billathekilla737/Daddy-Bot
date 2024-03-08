from Assets.F1_Functions import *
from Assets.Melee_Functions import *
from Assets.pStar_Names import *
from Assets.FlatFuckFriday import *
from Assets.Support import *
from discord import app_commands # type: ignore
from discord.ext import commands # type: ignore
import pytz
from tabulate import tabulate
from datetime import datetime, timedelta
convert_to_12hr = lambda time_str: datetime.strptime(time_str, '%H:%M').strftime('%I:%M %p')

###############Bot Description#####################
#The goal of this bot is to give a new users a nickname from a list of names from a text file.
#The bot will also give the user a role from a list of roles from a text file.

def run_discord_bot():
    ###########Initialize Bot####################################
    #scrape_race_info()                                          #
    token, URL = Parse_Private()                                #
    Scrap_Names()                                               #
    Scrap_Melee()                                               #
    scrape_f1_races('https://f1calendar.com')
    intents = discord.Intents.all()                             #
    global sent                                                 #
                                                                #
                                                                #
    client = discord.Client(command_prefix='/',intents=intents) #
    #Set the bot's status                                       #
    tree = app_commands.CommandTree(client)                     #
    #bot = commands.Bot(command_prefix='/', intents=intents)    #
    nameList, roleList = Grab_Files()                           #
    RacesJson = 'Daddy-Bot-env/Assets/F1Information.json'
    
    #############################################################
    
    #################################-Bot Events-########################################
    @client.event
    async def on_ready():
        #Variable Initialization
        #####################################################################
        print('We have logged in as {0.user}'.format(client))
        await client.change_presence(activity=discord.Game('with your mom'))
        PrevEvent = "" 
        # Event = find_next_event(RacesJson) # type: ignore
        # days, hours, minutes = get_timedelta_to_next_event(RacesJson)
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
        correctednow = datetime.now(chi_tz)
        if correctednow.hour < 3 or correctednow.hour > 6:
            await devchannel.send("I had an unscheduled restart!!! at " + str(correctednow))
            pass







        #   RECURRING TASKS (45 sec Loop)
        #####################################################################
        while True:
            #F1 Race Reminders
            #################################################################
            shouldSendF1Reminder = IsRaceTime(RacesJson)
            next_event = find_next_event(RacesJson) 
            days, hours, minutes = get_timedelta_to_next_event(RacesJson)
            timedelta_str = f"{days} days, {hours}:{minutes:02d} hours from now"
            if shouldSendF1Reminder and PrevEvent != next_event['event_type']:

                if "Free Practice" in next_event['event_type']:
                    FreePracticeRole = discord.utils.get(client.guilds[0].roles, name="Free Practice")
                    await channel.send(f"{FreePracticeRole.mention} **{next_event['event_type']}** is in " + str(hours) + " hours and " + str(minutes) + " minutes!")
                    PrevEvent = next_event['event_type']

                #TODO: ADD SPRINT AND SPRIINT SHOOTOUT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #TODO: Make TimeDelta Event Based
                

                elif "Qualifying" in next_event['event_type'] or "Sprint" in next_event['event_type']:
                    QualifyingRole = discord.utils.get(client.guilds[0].roles, name="Qualifying")
                    await channel.send(f"{QualifyingRole.mention} **{next_event['event_type']}** is in " + str(hours) + " hours and " + str(minutes) + " minutes!")
                    PrevEvent = next_event['event_type']
                             
                elif ("Grand Prix Grand Prix" in next_event['event_type']):
                    GrandPrix = discord.utils.get(client.guilds[0].roles, name="Grand Prix")
                    PrevEvent = next_event['event_type']
                    next_event['event_type'] = next_event['event_type'][:-10]
                    await channel.send(f"{GrandPrix.mention} **{next_event['event_type']}** is in " + str(hours) + " hours and " + str(minutes) + " minutes!")
                    

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
    @tree.command(name="freepractice", description="Tells you the next F1 free practice event <:f1_logo:1132150006988673034>")
    async def freepractice(interaction: discord.Interaction, practice_number: str):
        NextFP1 = find_next_event_by_type(RacesJson, "Free Practice 1")
        if NextFP1 != None:
            NextFP = NextFP1
        NextFP2 = find_next_event_by_type(RacesJson, "Free Practice 2")
        if NextFP2 != None:
            NextFP = NextFP2
        NextFP3 = find_next_event_by_type(RacesJson, "Free Practice 3")
        if NextFP3 != None:
            NextFP = NextFP3
        if NextFP != None:
            await interaction.response.send_message('The Next Practice #' + practice_number + ' is: ' + next_event['event_type'] + ' on ' + next_event['date'] + ' at ' + convert_to_12hr(next_event['time']))
        else:
            await interaction.response.send_message(f"Free Practice, Not Found")

    @tree.command(name = "qualifying", description = "Tells you the next F1 qualifying event")
    async def qualifying(interaction: discord.Interaction):
        #<:f1_logo:1132150006988673034>
        NextQualifying = find_next_event_by_type(RacesJson, "Qualifying")
        if NextQualifying != None:
            await interaction.response.send_message(f"The next F1 **Qualifying** event is on **{NextQualifying['date']} at {NextQualifying['time']}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"Qualifying, Not Found. Tell Zack...or don't. I don't care.")


    @tree.command(name = "sprintshootout", description = "Tells you the next F1 sprint shootout event")
    async def sprintshootout(interaction: discord.Interaction):
        NextSprintShootout = find_next_event_by_type(RacesJson, "Sprint Shootout")
        if NextSprintShootout != None:
            await interaction.response.send_message(f"The next F1 **Sprint Shootout** event is on **{NextSprintShootout['date']} at {NextSprintShootout['time']}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"Sprint Shootout, Not Found. Tell Zack...or don't. I don't care.")

    @tree.command(name = "sprint", description = "Tells you the next F1 sprint event")
    async def sprint(interaction: discord.Interaction):
        NextSprint = find_next_event_by_type(RacesJson, "Sprint")
        if NextSprint != None:
            await interaction.response.send_message(f"The next F1 **Sprint** event is on **{NextSprint['date']} at {NextSprint['time']}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"Sprint, Not Found. Tell Zack...or don't. I don't care.")
       
    @tree.command(name = "grandprix", description = "Tells you the next F1 Grand Prix event")
    async def grandprix(interaction: discord.Interaction):
        NextGrandPrix = find_next_event_by_type(RacesJson, "Grand Prix Grand Prix")
        if NextGrandPrix != None:
            await interaction.response.send_message(f"The next F1 **Grand Prix** event is on **{NextGrandPrix['date']} at {NextGrandPrix['time']}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"Grand Prix, Not Found. Tell Zack...or don't. I don't care.")

    @tree.command(name="help", description="Tells you the commands for the bot")
    async def help(interaction: discord.Interaction):
        # Define the table headers
        headers = ["Command", "Description"]
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
        table = tabulate(rows, headers=headers, tablefmt="pipe")
        await interaction.response.send_message(f"Here are the available commands:\n\n```{table}```")

    @tree.command(name = "nextevent", description = "Tells you the next F1 Event <:f1_logo:1132150006988673034>")
    async def nextevent(interaction: discord.Interaction):
        days, hours, minutes = get_timedelta_to_next_event(RacesJson)
        timedelta_str = f"{days} days, {hours} hours, {minutes:02d} minutes"
        nextevent = find_next_event(RacesJson)
        await interaction.response.send_message(f"The next F1 event is **{nextevent['event_type']}** on **{nextevent['date']} at {nextevent['time']}** <a:max_nice:1117178831120371824> \n T-minus {timedelta_str} until the next event!")
    #############################################################################################################################################
    #TODO FIX WEEK COMMAND
    # @tree.command(name = "week", description = "Tells you the next F1 events for the week <:f1_logo:1132150006988673034>")
    # async def week(interaction: discord.Interaction):
    #     FreePractice1Date, FreePractice1Time    = find_next_event_by_type(RacesJson, "Free Practice 1")
    #     FreePractice2Date, FreePractice2Time    = find_next_event_by_type(RacesJson, "Free Practice 2")
    #     FreePractice3Date, FreePractice3Time    = find_next_event_by_type(RacesJson, "Free Practice 3")
    #     QualifyingDate, QualifyingTime          = find_next_event_by_type(RacesJson, "Qualifying")
    #     SprintDate, SprintTime                  = find_next_event_by_type(RacesJson, "Sprint")
    #     SprintShootoutDate, SprintShootoutTime  = find_next_event_by_type(RacesJson, "Sprint Shootout")
    #     GrandPrixDate, GrandPrixTime            = find_next_event_by_type(RacesJson, "Grand Prix")
    #     Next_Location                           = str(find_json_Next_Event_Location())
    #     Next_Location                           = Next_Location[:-4]

    #     print(FreePractice2Time)
    #     headers = ["Location", "Event", "Date", "Time"]
    #     #If it is not a sprint shootout weekend
    #     if FreePractice2Time == None:
    #         rows = [
    #             [Next_Location, "Free Practice 1", FreePractice1Date, FreePractice1Time],
    #             [Next_Location, "Qualifying", QualifyingDate, QualifyingTime],
    #             [Next_Location, "Sprint Shootout", SprintShootoutDate, SprintShootoutTime] if SprintShootoutDate else None,
    #             [Next_Location, "Sprint", SprintDate, SprintTime] if SprintDate else None,
    #             [Next_Location, "Grand Prix", GrandPrixDate, GrandPrixTime]
    #         ]
                
    #     #If it is a sprint shootout weekend
    #     elif FreePractice2Time != None:
    #         rows = [
    #             [Next_Location, "Free Practice 1", FreePractice1Date, FreePractice1Time],
    #             [Next_Location, "Free Practice 2", FreePractice2Date, FreePractice2Time],
    #             [Next_Location, "Free Practice 3", FreePractice3Date, FreePractice3Time],
    #             [Next_Location, "Qualifying", QualifyingDate, QualifyingTime],
    #             [Next_Location, "Sprint Shootout", SprintShootoutDate, SprintShootoutTime] if SprintShootoutDate else None,
    #             [Next_Location, "Sprint", SprintDate, SprintTime] if SprintDate else None,
    #             [Next_Location, "Grand Prix", GrandPrixDate, GrandPrixTime]
    #         ]


    #     rows = [row for row in rows if row is not None]
    #     table = tabulate(rows, headers=headers, tablefmt="pipe")
    #     await interaction.response.send_message(f"```{table}```")








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



