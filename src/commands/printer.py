import discord
from discord.ext import commands
from discord import app_commands

def setup(client: commands.Bot):
    @client.tree.command(name="printer", description="copy message")
    async def printer(interaction: discord.Interaction, printer: str):
        await interaction.response.send_message(printer)
