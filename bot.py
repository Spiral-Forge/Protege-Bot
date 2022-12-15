import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents = intents)

#memberlist has the entire list of the server members
memberlist = []

def printMembers(member):
    memberlist.append(member.name+'#'+member.discriminator)
    #print(memberlist) to print the entire list


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

client.run(os.getenv('TOKEN'))