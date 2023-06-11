from DaddyBot import tree
from F1_Functions import *

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
        await interaction.response.send_message(f"the next F1 qualifying event is on {date} at {time}")
    else:
        date, time = find_next_of_type("Sprint",None)
        await interaction.response.send_message(f"There is NO qualifying, SPRINT is on {date} at {time}")
@tree.command(name = "sprint", description = "Tells you the next F1 sprint event")
async def sprint(interaction: discord.Interaction):
    date, time = find_next_of_type("Sprint",None)
    if date and time != None:
        await interaction.response.send_message(f"The next F1 sprint event is on {date} at {time}")
    else:
        date, time = find_next_of_type("Qualifying",None)
        await interaction.response.send_message(f"There is NO sprint, QUALIFYING is on {date} at {time}")
@tree.command(name = "grandprix", description = "Tells you the next F1 Grand Prix event")
async def grandprix(interaction: discord.Interaction):
    date, time = find_next_of_type("Grand Prix",None)
    await interaction.response.send_message(f"The next F1 Grand Prix event is on {date} at {time}")
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
        await interaction.response.send_message('The next F1 Event is at ' + Next_Location + f' dates and times are: \n\nFree Practice 1 on {FreePractice1Date} at {FreePractice1Time} \nFree Practice 2 on {FreePractice2Date} at {FreePractice2Time} \nFree Practice 3 on {FreePractice3Date} at {FreePractice3Time} \nQualifying on {QualifyingDate} at {QualifyingTime} \nGrand Prix on {GrandPrixDate} at {GrandPrixTime}')
    else:
        await interaction.response.send_message('The next F1 Event is at ' + Next_Location + f' dates and times are: \n\nFree Practice 1 on {FreePractice1Date} at {FreePractice1Time} \nFree Practice 2 on {FreePractice2Date} at {FreePractice2Time} \nFree Practice 3 on {FreePractice3Date} at {FreePractice3Time} \nSprint on {SprintDate} at {SprintTime} \nGrand Prix on {GrandPrixDate} at {GrandPrixTime}')
