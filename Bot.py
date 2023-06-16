import discord
from discord import app_commands
from discord.ext import commands
import responses
from responses import date_range_list
import ProfanityList
from ProfanityList import profanityList


async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message)
        #sends a list as individual messages
        if isinstance(response, list):
            await message.channel.send('## React to Dates That You Are Available For:')
            for i in response:
                await message.channel.send(f'* {i}')
        #sending of other forms of messages
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    #put the bot's individual token here
    TOKEN = "<<TOKEN>>"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        print(f'{client.user} is now going')

    @client.event
    async def on_message(message):
        user_message = str(message.content)
        #username = str(message.author)
        #channel = str(message.channel)
        if message.author == client.user and user_message.count(',') == 2:
            await message.add_reaction("✅")
            await message.add_reaction("⚠️")
            await message.add_reaction("🚫")

        #If you want print messages for all messages sent
        #print(f'{username} said: "{user_message}" in {channel}')
    
    @tree.command(name='sync', description='Owner only')
    async def sync(interaction: discord.Interaction):
        #Put you
        if interaction.user.id == "<<USER_ID>>":
            await tree.sync()
            print('Command tree synced.')
        else:
            await interaction.response.send_message('You must be the owner to use this command!')
                                                    
    @tree.command(name = "eventpoll", description = "Make a Poll for Available Dates from Given Date Ranges")
    @app_commands.describe(event_name = "Type the name of the event")
    @app_commands.describe(people = "@ the individuals/roles who you want to notify of the vote")
    @app_commands.describe(first_date = "What's the First Potential Date in mm/dd/yyyy")
    @app_commands.describe(second_date = "What's the Second Potential Date in mm/dd/yyyy")
    async def eventpoll(interaction: discord.Interaction, event_name: str, people: str, first_date: str, second_date: str):
        funny = (f'{event_name} {people}').lower()
        if any(word in funny for word in profanityList):
            await interaction.response.send_message ('No Profanity of Any Kind')
        else:
            dateList = date_range_list(first_date, second_date)
            if isinstance(dateList, list):
                await interaction.response.send_message (f'## {event_name}\n### React to Dates That You Are Available For: {people}\n### ✅ For Days You Can Attend | ⚠️ For Days You Might Be Able to Attend or Have Time Constraints | 🚫 For Days You Can\'t Attend')
                for i in dateList:
                    await interaction.channel.send(f'* {i}')
            else:
                await interaction.response.send_message (dateList)


    client.run(TOKEN)
