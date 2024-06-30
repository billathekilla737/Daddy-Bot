from Assets.F1_Functions import *
from Assets.pStar_Names import *
from Assets.FlatFuckFriday import *
from Assets.Support import *
from discord import app_commands # type: ignore
from discord.ext import commands # type: ignore
#import pytz
from tabulate import tabulate
from datetime import datetime, timedelta




def convert_to_12hr(time_str):
    if time_str == 'Completed':
        return 'Completed'
    else:
        return datetime.strptime(time_str, '%H:%M').strftime('%I:%M %p')
    
def convert_date(date_str):
    return datetime.strptime(date_str, "%d %b").strftime("%d %B")

###############Bot Description#####################
#The goal of this bot is to give a new users a nickname from a list of names from a text file.
#The bot will also give the user a role from a list of roles from a text file.

def run_discord_bot():
    ###########Initialize Bot####################################
                                                                #
    token, URL = Parse_Private()                                #
    Scrap_Names()                                               #
    scrape_f1_races('https://f1calendar.com')                   #
    intents = discord.Intents.all()                             #
    global sent                                                 #
                                                                #
                                                                #
    client = discord.Client(command_prefix='/',intents=intents) #
    #Set the bot's status                                       #
    tree = app_commands.CommandTree(client)                     #
                                                                #
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
        channel = client.get_channel(907764974099787797)#F1 Channel
        #channel = client.get_channel(1115817757267730533)#TEST CHANNEL
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

                event_type = next_event['event_type']
                if "Free Practice" in event_type:
                    FreePracticeRole = discord.utils.get(client.guilds[0].roles, name="Free Practice")
                    await channel.send(f"{FreePracticeRole.mention} The **{event_type}** is in {hours} hours and {minutes} minutes!")
                    PrevEvent = event_type

                elif "Sprint Qualifying" in event_type:
                    SprintQualifyingRole = discord.utils.get(client.guilds[0].roles, name="Sprint Qualifying")
                    await channel.send(f"{SprintQualifyingRole.mention} The **{event_type}** is in {hours} hours and {minutes} minutes!")
                    PrevEvent = event_type

                elif "Sprint" in event_type:
                    SprintRole = discord.utils.get(client.guilds[0].roles, name="Sprint")
                    await channel.send(f"{SprintRole.mention} The **{event_type}** is in {hours} hours and {minutes} minutes!")
                    PrevEvent = event_type

                elif "Qualifying" in event_type or "Sprint" in event_type:
                    QualifyingRole = discord.utils.get(client.guilds[0].roles, name="Qualifying")
                    await channel.send(f"{QualifyingRole.mention} The **{event_type}** is in {hours} hours and {minutes} minutes!")
                    PrevEvent = event_type
                             
                elif "Grand Prix Grand Prix" in event_type:
                    GrandPrixRole = discord.utils.get(client.guilds[0].roles, name="Grand Prix")
                    PrevEvent = event_type
                    event_type = event_type.replace(" Grand Prix", "")
                    await channel.send(f"{GrandPrixRole.mention} The **{event_type} Grand Prix** is in {hours} hours and {minutes} minutes!")
                    

            #Melee Reminder (SHUT DOWN UNTIL A Better Site To Scrap Is Found)
            #################################################################
            # try:
            #     shouldSendMeleeReminder = isMeleeTime()
            # except Exception as e:
            #     print(f"{e}  Error in isMeleeTime()")
            #     shouldSendMeleeReminder = False
            
            # if shouldSendMeleeReminder and PrevMeleeEvent != MeleeEvent:
            #     MeleeRole = discord.utils.get(client.guilds[0].roles, name="Melee")
            #     #Message = f"{role.mention} {Event} is in {TimeDelta}!"
            #     await meleechannel.send(f"{MeleeRole.mention} {MeleeEvent} is Today!")
            #     PrevMeleeEvent = MeleeEvent

            #Flat Fuck Friday Reminder
            ################################################################
            if isFlatFuckFriday() and sent != True:
                #IT'S FLAT FUCK FRIDAY! :FlatFuck:
                #Send a message in General that it's Flat Fuck Friday!
                message = "<:FlatFuck:1117199409478914128> It's Flat Fuck Friday You Fucking Losers! <:FlatFuck:1117199409478914128> \nhttps://vimeo.com/921143035"
                GeneralChannel = client.get_channel(632027078371573775)
                await GeneralChannel.send(message)
                sent = True
                asyncio.create_task(reset_sent())
            await asyncio.sleep(30)
        

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
        NextFP = find_next_event_by_type(RacesJson, "Free Practice " + str(practice_number))
        #TODO: Make an Exception if it's end of season and no fp1, fp2, or fp3
        await interaction.response.send_message('The Next Practice #' + practice_number + ' is: ' + NextFP['event_type'] + ' on ' + NextFP['date'] + ' at ' + convert_to_12hr(NextFP['time']))


    @tree.command(name = "qualifying", description = "Tells you the next F1 qualifying event")
    async def qualifying(interaction: discord.Interaction):
        #<:f1_logo:1132150006988673034>
        NextQualifying = find_next_event_by_type(RacesJson, "Qualifying")
        if NextQualifying != None:
            await interaction.response.send_message(f"The next F1 **Qualifying** event is on **{NextQualifying['date']} at {NextQualifying['time']}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"Qualifying, Not Found. Tell Zack...or don't. I don't care.")


    @tree.command(name = "sprintqualifying", description = "Tells you the next F1 sprint Qualifying event")
    async def sprintQualifying(interaction: discord.Interaction):
        NextSprintQualifying = find_next_event_by_type(RacesJson, "Sprint Qualifying")
        if NextSprintQualifying != None:
            await interaction.response.send_message(f"The next F1 **Sprint Qualifying** event is on **{NextSprintQualifying['date']} at {NextSprintQualifying['time']}** <:f1_logo:1132150006988673034>")
        else:
            await interaction.response.send_message(f"Sprint Qualifying, Not Found. Tell Zack...or don't. I don't care.")

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
            ["/sprintqualifying", "Tells you the next F1 sprint Qualifying event"],
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
        await interaction.response.send_message(f"The next F1 event is **{nextevent['event_type']}** on **{nextevent['date']} at {convert_to_12hr(nextevent['time'])}** <a:max_nice:1117178831120371824> \n T-minus {timedelta_str} until the next event!")
    #############################################################################################################################################
    
    @tree.command(name = "week", description = "Tells you the next F1 events for the week <:f1_logo:1132150006988673034>")
    async def week(interaction: discord.Interaction):
        NextFP1                 = find_next_event_by_type(RacesJson, "Free Practice 1")
        NextFP2                 = find_next_event_by_type(RacesJson, "Free Practice 2")
        NextFP3                 = find_next_event_by_type(RacesJson, "Free Practice 3")
        NextQualifying          = find_next_event_by_type(RacesJson, "Qualifying")
        NextSprintQualifying    = find_next_event_by_type(RacesJson, "Sprint Qualifying")
        NextSprint              = find_next_event_by_type(RacesJson, "Sprint")
        NextGrandPrix           = find_next_event_by_type(RacesJson, "Grand Prix Grand Prix")
        Next_Location           = find_next_event(RacesJson)['event_type']
        pattern = r"^(.*?Grand Prix)"
        match = re.search(pattern, Next_Location)
        if match:
            Next_Location = match.group(1)
        else:
            print("Regex Match Not Found, Week Command")

        #Clean up and remove the Events where there data is already passed
        ###############################################################################

        #Check if the event exist for the current week and if it has already passed.
        #If it has, then mark it as completed
        events = [NextFP1, NextFP2, NextFP3, NextSprintQualifying, NextSprint, NextQualifying]

        for event in events:
            if event is not None and Next_Location not in event['event_type']:
                event['date'] = 'Completed'
                event['time'] = 'Completed'

        

        headers = ["Location", "Event", "Date", "Time"]
        print(f"The Next Sprint Qualifying is: {NextSprintQualifying}, the Next Location is: {Next_Location}")
        if NextSprint['event_type'][:-11] == Next_Location:
            print(NextSprint['event_type'][:-11])
            print(Next_Location)
            print(NextSprintQualifying)
        else:
            print('Else Statement')
            print(NextSprint['event_type'][:-11])
            print(Next_Location)
            print(NextSprintQualifying)
        
        if (NextSprintQualifying != None and NextSprint['event_type'][:-11] == Next_Location) or NextSprintQualifying['time'] == 'Completed':
            rows = [
                [Next_Location, "Free Practice 1", NextFP1['date'], convert_to_12hr(NextFP1['time'])],
                [Next_Location, "Free Practice 2", NextFP2['date'], convert_to_12hr(NextFP2['time'])],
                [Next_Location, "Free Practice 3", NextFP3['date'], convert_to_12hr(NextFP3['time'])],
                [Next_Location, "Sprint Qualifying", NextSprintQualifying['date'], convert_to_12hr(NextSprintQualifying['time'])],
                [Next_Location, "Sprint", NextSprint['date'], convert_to_12hr(NextSprint['time'])],
                [Next_Location, "Qualifying", NextQualifying['date'], convert_to_12hr(NextQualifying['time'])],
                [Next_Location, "Grand Prix", NextGrandPrix['date'], convert_to_12hr(NextGrandPrix['time'])]
            ]
        else:
            rows = [
                [Next_Location, "Free Practice 1", NextFP1['date'], convert_to_12hr(NextFP1['time'])],
                [Next_Location, "Free Practice 2", NextFP2['date'], convert_to_12hr(NextFP2['time'])],
                [Next_Location, "Free Practice 3", NextFP3['date'], convert_to_12hr(NextFP3['time'])],
                [Next_Location, "Qualifying", NextQualifying['date'], convert_to_12hr(NextQualifying['time'])],
                [Next_Location, "Grand Prix", NextGrandPrix['date'], convert_to_12hr(NextGrandPrix['time'])]
            ]
        rows = [row for row in rows if row[1] != None]
        table = tabulate(rows, headers=headers, tablefmt="pipe")
        await interaction.response.send_message(f"Here are the next F1 events for the week:\n\n```{table}```")


    #Reaction Roles
    ##############################################################################################################################################
    #Shutting Down Melee Reaction Roles for now
    #@client.event
    # async def on_raw_reaction_add(payload):
    #     meleechannel = client.get_channel(1117158502989844600)
    #     if payload.emoji.name == "🥊" and payload.message_id == 1119503042144911440 and payload.channel_id == meleechannel.id:
    #         guild = await client.fetch_guild(payload.guild_id)
    #         member = await guild.fetch_member(payload.user_id)
    #         role = discord.utils.get(guild.roles, name="Melee")
    #         await member.add_roles(role)

    # @client.event
    # async def on_raw_reaction_remove(payload):
    #     meleechannel = client.get_channel(1117158502989844600)
    #     if payload.emoji.name == "🥊" and payload.message_id == 1119503042144911440 and payload.channel_id == meleechannel.id:
    #         guild = await client.fetch_guild(payload.guild_id)
    #         member = await guild.fetch_member(payload.user_id)
    #         role = discord.utils.get(guild.roles, name="Melee")
    #         await member.remove_roles(role)
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



