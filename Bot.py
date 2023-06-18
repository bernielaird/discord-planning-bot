import configparser
import json
from datetime import datetime, timezone

import boto3
import discord
from botocore.exceptions import ClientError
from discord import app_commands

import responses
from ProfanityList import profanityList
from responses import date_range_list


async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message)
        # sends a list as individual messages
        if isinstance(response, list):
            await message.channel.send('## React to Dates That You Are Available For:')
            for i in response:
                await message.channel.send(f'* {i}')
        # sending of other forms of messages
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


def get_secrets_client():
    try:
        config = configparser.ConfigParser()
        config.read("local.cnf")
        profile_name = config.get('aws', 'profile_name')

        # Create a Secrets Manager client
        session = boto3.session.Session(
            profile_name=profile_name
        )
    except Exception as e:
        session = boto3.session.Session()

    region_name = "us-west-2"

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    return client


def get_secrets():
    client = get_secrets_client()
    print(f'got client ok')

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId="prod/discord"
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    print(f'got secrets response ok')

    # Decrypts secret using the associated KMS key.
    secrets_string = get_secret_value_response['SecretString']
    return json.loads(secrets_string)


def start_discord_bot():
    secrets = get_secrets()
    token = secrets['discord_token']
    user_id = int(secrets['discord_user_id'])
    run_discord_bot(token=token, user_id=user_id)


def run_discord_bot(token, user_id):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        now_utc = datetime.now(timezone.utc)
        print(f'{client.user} started at: {now_utc}')

    @client.event
    async def on_message(message):
        user_message = str(message.content)
        # username = str(message.author)
        # channel = str(message.channel)
        if message.author == client.user and user_message.count(',') == 2:
            await message.add_reaction("✅")
            await message.add_reaction("⚠️")
            await message.add_reaction("🚫")

        # If you want print messages for all messages sent
        # print(f'{username} said: "{user_message}" in {channel}')

    @tree.command(name='sync', description='Owner only')
    async def sync(interaction: discord.Interaction):
        if interaction.user.id == user_id:
            await tree.sync()
            print('Command tree synced.')
        else:
            await interaction.response.send_message('You must be the owner to use this command!')

    @tree.command(name="eventpoll", description="Make a Poll for Available Dates from Given Date Ranges")
    @app_commands.describe(event_name="Type the name of the event")
    @app_commands.describe(people="@ the individuals/roles who you want to notify of the vote")
    @app_commands.describe(first_date="What's the First Potential Date in mm/dd/yyyy")
    @app_commands.describe(second_date="What's the Second Potential Date in mm/dd/yyyy")
    async def eventpoll(interaction: discord.Interaction,
                        event_name: str,
                        people: str,
                        first_date: str,
                        second_date: str):
        funny = (f'{event_name} {people}').lower()
        if any(word in funny for word in profanityList):
            await interaction.response.send_message('No Profanity of Any Kind')
        else:
            dateList = date_range_list(first_date, second_date)
            if isinstance(dateList, list):
                await interaction.response.send_message(
                    f'## {event_name}\n### React to Dates That You Are Available For: {people}\n### ✅ For Days You Can Attend | ⚠️ For Days You Might Be Able to Attend or Have Time Constraints | 🚫 For Days You Can\'t Attend')
                for i in dateList:
                    await interaction.channel.send(f'* {i}')
            else:
                await interaction.response.send_message(dateList)

    client.run(token)
