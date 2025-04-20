import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands import register_all_commands 

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = discord.Object(id=int(os.getenv("DISCORD_SERVER_ID")))

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try:
             synced = await client.tree.sync()
             print(f'Synced {len(synced)} global commands.')
        except Exception as e:
             print(f'Error syncing commands: {e}')

async def on_message(self, message):
    if message.author == self.user:
            return
    if message.content.startswith('traktor'):
        print(f'Message from {message.author}: {message.content}')
        await message.channel.send('balls')

client = Client(command_prefix="!", intents=intents)

# Register slash commands from all files
register_all_commands(client)

client.run(TOKEN)
