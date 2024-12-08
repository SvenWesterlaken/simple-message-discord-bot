import discord
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    print(message.channel)

    if message.author == client.user or message.author.bot:
        # We don't answer to bots or if we are logged in as the bot
        return

    createdThread = await message.create_thread(
        name=message.content, 
        reason='Question: ' + message.content
    )

    async with createdThread.typing():
        # simulate something heavy
        await asyncio.sleep(10)

    # Send back the legnth of the message together with the users name
    await createdThread.send('Hi, ' + message.author.name + '! Your message was ' + str(len(message.content)) + ' characters long.')

# Run the client with the API key from the environment set
client.run(os.getenv('DISCORD_API_KEY'));
