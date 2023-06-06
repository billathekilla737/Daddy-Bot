import sys
#Vivenv pathing issue. Hacky Fix.
sys.path.append(r'c:\users\zacha\appdata\local\programs\python\python310\lib\site-packages')
import discord
from DaddyBot import on_member_join

# Create a mock member object
member = discord.Member()
member.name = "TestUser"
member.id = 1234567890

# Call the on_member_join event handler
on_member_join(member)