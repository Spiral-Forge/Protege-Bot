import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
from pandas import *

load_dotenv()
intents = discord.Intents.all()
intents.members = True 
client = commands.Bot(command_prefix = "!", intents = intents)

#memberlist has the entire list of the server members
memberlist = []

def convertCSVtoList():
    data = read_csv("Protege.csv")
    global mentors
    mentors = data['Mentors'].tolist()
    global mentees
    mentees = data['Mentees'].tolist()


def printMembers(member):
    memberlist.append(member.name+'#'+member.discriminator)


@client.event
async def on_ready():
      print("Server Up")

# errors handled in code
@client.command()
async def printID(ctx, *, message = None):
    if message != None:
        members = ctx.guild.members
        for member in members:
            try:
                await printMembers(member)
            except:
                pass
    else:
        await ctx.send("Error occured")

@client.command()
async def members_roles(ctx, *, message = None):
    convertCSVtoList()
    if message != None:
        for member in memberlist:
            if member in mentees:
                #try:
                    guild = await client.fetch_guild(1047577694428209182)
                    user = guild.get_member_named(member)
                    role = guild.get_role(1048825310348583022)
                    await user.add_roles(role)
                #except:
                    #pass
            elif member in mentors:
                #try:
                    guild = await client.fetch_guild(1047577694428209182)
                    user = guild.get_member_named(member)
                    role = guild.get_role(1048825107277160468)
                    await user.add_roles(role)  
                #except:
                    #pass
    else:
        await ctx.send("Error occured")

client.run(os.getenv('TOKEN'))