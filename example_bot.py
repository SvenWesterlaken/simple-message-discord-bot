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
        thread = await interaction.channel.create_thread(
            name='Question: ' + interaction.user.name,
            reason='Question: ' + interaction.user.name,
            type=discord.ChannelType.private_thread
        )

        await thread.add_user(interaction.user)

        if button:
            await interaction.response.send_message('Thread created, you can ask your question there.', ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction):
        # We can add a check if we want to block the interaction for non-admins
        return True

@client.event
async def on_ready():
    print(f'We have logged in as "{client.user}"')

@client.command()
@commands.has_permissions(administrator=True)
async def init(ctx: commands.Context):
    await ctx.message.delete() # Delete the command message
    await ctx.channel.purge() # Clear the channel

    embed = discord.Embed(
        title = 'Welcome to the Question Setup',
        description = 'Click the button below to ask a question.',
        color = discord.Color.blurple()
    )

    await ctx.send(
        embed = embed,
        view = QuestionSetupView()
    )

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx: commands.Context):
    await ctx.channel.purge()

    for thread in ctx.channel.threads:
        await thread.delete()

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user or message.author.bot:
        # We don't answer to bots or if we are logged in as the bot
        return

    if message.content.startswith('!mr') and message.channel.name == 'ask-channel':
        # Only process commands if they start with prefix (so we don't init interactions on messages)
        # and only in the ask-channel
        await client.process_commands(message)

    channel = message.channel

    if channel.type is not discord.ChannelType.private_thread:
        # We don't answer outside of the context of a private thread
        return

    if channel.parent.name != 'ask-channel':
        # We only answer in the context of a thread in the ask-channel channel
        return
    
    messagesInThread = [m async for m in channel.history(limit=2, oldest_first=True)]

    if len(messagesInThread) > 0:
        # The first message was the adding of the user to the thread
        # TODO: might need a filtering for the bot messages and then get the first one
        # but we should find a sweet spot for the filtering as we need more than one message in that case
        firstMessage = messagesInThread[1]

        if len(firstMessage.content) > 50:
            # If the message is longer than 50 characters, we shorten it
            name = firstMessage.content[:50] + '...'
        else:
            name = firstMessage.content

        await channel.edit(name=name)

    async with channel.typing():
        # simulate something heavy
        await asyncio.sleep(5)

    # Send back the legnth of the message together with the users name
    await message.reply('Hi, ' + message.author.name + '! Your message was ' + str(len(message.content)) + ' characters long.')

# Run the client with the API key from the environment set
client.run(os.getenv('DISCORD_API_KEY'));
