import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!mr ', intents=intents)

class QuestionSetupView(discord.ui.View):

    def __init__(self):
        super().__init__()

        # Make sure we have no timeout
        self.timeout = None

    @discord.ui.button(label='Ask a Question', style=discord.ButtonStyle.blurple)
    async def ask_question(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('You asked a question!')

    async def interaction_check(self, interaction: discord.Interaction):
        # We can add a check if we want to block the interaction for non-admins
        return True

@client.event
async def on_ready():
    print(f'We have logged in as "{client.user}"')
    # await discordClient.tree.sync()

@client.command()
@commands.has_permissions(administrator=True)
async def initialize(ctx):
    await ctx.message.delete()
    await ctx.channel.purge()

    await ctx.send(
        view = QuestionSetupView()
    )

# @client.event
# async def on_message(message):
#     print(message)

#     if message.author == client.user or message.author.bot:
#         # We don't answer to bots or if we are logged in as the bot
#         return

#     if message.channel.type == 'public_thread' or 'private_thread':
#         thread = message.channel
#     else:
#         thread = await message.create_thread(
#             name=message.content, 
#             reason='Question: ' + message.content
#         )

#     async with thread.typing():
#         # simulate something heavy
#         await asyncio.sleep(10)

#     # Send back the legnth of the message together with the users name
#     await thread.send('Hi, ' + message.author.name + '! Your message was ' + str(len(message.content)) + ' characters long.')

# Run the client with the API key from the environment set
client.run(os.getenv('DISCORD_API_KEY'));
