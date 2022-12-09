import discord
import csv
import discord.utils
from discord.ext import commands
import os

intents = discord.Intents.default()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    with open(os.getenv('CSV'), mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            user_id = row['user_id']
            role_id = row['role_id']
            user =discord.utils.find(lambda u: u.id == int(user_id), client.get_all_members())
            role =discord.utils.get(user.guild.roles, id=int(role_id))
            await user.add_roles(role)
            print(f'Role {role.name} has been added to {user.name}')
 
client.run(os.getenv('TOKEN'))
