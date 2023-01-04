import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
from pandas import *
from discord import Member

load_dotenv()
intents = discord.Intents.all()
intents.members = True 
client = commands.Bot(command_prefix = "!", intents = intents)

#memberlist has the entire list of the server members
memberlist = []
member_disc = []
member_names = []
memberids = []

#mentor details 
mentor_disc = []
mentor_names = []
mentorids = []

#mentee details
mentee_disc = []
mentee_names = []
menteeids = []


def convertCSVtoList():
    data = read_csv("Protege.csv")
    global mentors
    mentors = data['Mentors'].tolist()
    global mentees
    mentees = data['Mentees'].tolist()
    print("-----")
    print(mentors)
    print(mentees)


def userListsToIDLists():
    for mentor in mentors:
        mentor_disc.append(mentor[-4:])
        mentor_names.append(mentor[:-5])
        

    for mentee in mentees:
        mentee_disc.append(mentee[-4:])
        mentee_names.append(mentee[:-5])

    for member in memberlist:
        member_disc.append(member[-4:])
        member_names.append(member[:-5])

    print('1: ', mentor_names)
    print('2: ', mentor_disc)
    print('3: ', mentee_names)
    print('4: ', mentee_disc)
    print('5: ', member_names)
    print('6: ', member_disc)


def convertToIDs():
    for i in range(0,len(mentor_names)):
        id = discord.utils.get(client.get_all_members(), name=mentor_names[i], discriminator=mentor_disc[i]).id
        mentorids.append(id)

    for i in range(0,len(mentee_names)):
        id = discord.utils.get(client.get_all_members(), name=mentee_names[i], discriminator=mentee_disc[i]).id
        menteeids.append(id)


    for i in range(0,len(member_names)):
        id = discord.utils.get(client.get_all_members(), name=member_names[i], discriminator=member_disc[i]).id
        memberids.append(id)

    print("mentorids: ", mentorids)
    print("menteeids: ", menteeids)
    print("memberids: ", memberids)

def printMembers(member):
    memberlist.append(member.name+'#'+member.discriminator)
    print(memberlist)

async def member_roles(person, role_id):
    guild = client.get_guild(1047577694428209182)
    #discord.guild.guild type
    print(type(guild))
    print(guild.roles)
    role = discord.utils.get(guild.roles, id = role_id)
    #discord.role.role type
    print(type(role))
    member = guild.get_member(person)
    #discord.member.member type
    print(member)
    print(type(member))
    await member.add_roles(role)

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
async def generateLists(ctx, *, message = None):
    convertCSVtoList()
    userListsToIDLists()
    convertToIDs()

@client.command()
async def add_roles(ctx):
    for mem in memberids:
        if mem in mentorids:
            await member_roles(mem,1048824533810946048)
        if mem in menteeids:
            await member_roles(mem,1048843590316589066)

client.run(os.getenv('TOKEN'))