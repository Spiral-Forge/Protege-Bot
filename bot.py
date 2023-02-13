import discord
import csv
import math
from discord.ext import commands
from discord.utils import get
import os
import pickle
import os.path
from dotenv import load_dotenv
from pandas import *
from discord import Member
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List
from google.oauth2 import service_account
import numpy as np

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv()
TOKEN = os.getenv('TOKEN')
SAMPLE_SPREADSHEET_ID = '1A_HLCmn2colzXV4-6COTT18QWeoCSSImtXnd1p1VrCQ'

intents = discord.Intents.all()
intents.members = True 
client = commands.Bot(command_prefix = "!", intents = intents)
creds = None
creds = service_account.Credentials.from_service_account_file('keys.json', scopes=SCOPES)


service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

memberlist = []
member_disc = []
member_names = []
memberids = []
member_role = []
#mentor details 
mentor_disc = []
mentor_names = []
mentorids = []
mentor_role = [] 

#mentee details
mentee_disc = []
mentee_names = []
menteeids = []
mentee_role = [] 

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
    print('-=-=-=-=-=-=3-=-3=3-=3-=2-3=12-4=34-=12-4=32-4=12')
    for mentor in mentors:
        print(mentor)
        mentor_disc.append(mentor[-4:])
        mentor_names.append(mentor[:-5])
        print(mentor_names)
        
    print('-=-=-=-=-=-=3-=-3=3-=3-=2-3=12-4=34-=12-4=32-4=12')
    for mentee in mentees:
        print(mentee)
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
        print(mentor_names[i], mentor_disc[i])
        print('-----------------x-x-x-x--------------', type(discord.utils.get(client.get_all_members(), name=mentor_names[i], discriminator=mentor_disc[i])))
        id = discord.utils.get(client.get_all_members(), name=mentor_names[i], discriminator=mentor_disc[i]).id
        mentorids.append(id)

    for i in range(0,len(mentee_names)):
        print(mentee_names[i], mentee_disc[i])
        print('-----------------x-x-x-x--------------', type(discord.utils.get(client.get_all_members(), name=mentee_names[i], discriminator=mentee_disc[i])))
        id = discord.utils.get(client.get_all_members(), name=mentee_names[i], discriminator=mentee_disc[i]).id
        menteeids.append(id)


    for i in range(0,len(member_names)):
        id = discord.utils.get(client.get_all_members(), name=member_names[i], discriminator=member_disc[i]).id
        memberids.append(id)

    print("mentorids: ", mentorids)
    print("menteeids: ", menteeids)
    print("memberids: ", memberids)

def printMembers(member):
    memberlist.append(member.name +'#'+ member.discriminator)
    #return memberlist
    print(memberlist)
    #if condition
    print('===================================================',type(member))


@client.command()
async def print_roles(ctx, *, message = None):
    channel = await client.fetch_channel(1073968826993090603) #gets the channel you want to get the list from
    #print(type(channel))
    members1 = channel.members #finds members connected to the channel
    for member in members1:
        mentor_role.append(member.name  + '#' + member.discriminator)
    print(mentor_role) #print info
    # print(members1)
    channel1 = await client.fetch_channel(1073969129167519754) #gets the channel you want to get the list from
    #print(type(channel))
    members2 = channel1.members #finds members connected to the channel
    for member in members2:
        mentee_role.append(member.name  + '#' + member.discriminator)
    print(mentee_role) #print info
    # print(members1)

async def member_roles(person, role_id):
    guild = client.get_guild(931459573003472946)
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
            #if the member has a role 
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
            await member_roles(mem,1074350860152340573)
            member_role.append(mem)
        if mem in menteeids:
            await member_roles(mem,1074351703014518786)
            member_role.append(mem)
    print(member_role)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

@client.command(name='generateCSV')
async def testCommand(ctx, *args):
    if (len(args) == 0):
        await ctx.send("Please send some arguements!")
    else:
    
        valuesToWrite = [
            mentor_role,
        ]
        valuesToWrite1 = [
            mentee_role,   
        ]
      
        body = {
            'values': valuesToWrite
        }
        body2 = {
            'values': valuesToWrite1
        }
        
        sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Mentors!A1", valueInputOption='USER_ENTERED', body=body).execute()
        sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Mentees!A1", valueInputOption='USER_ENTERED', body=body2).execute()


@client.command()
async def add_old_role(ctx):
    count = 0
    members = ctx.guild.members
    for member in members: 
        await member_roles(member.id, 1061605398089568286)
        count=count+1
        print(count)

    print('-------------------------Done!----------------------', count)

client.run(os.getenv('TOKEN'))



        
