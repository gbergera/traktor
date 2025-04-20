import discord
from discord.ext import commands
from discord import app_commands

def setup(client: commands.Bot):
    @client.tree.command(name="balls", description="just do it")
    async def say_balls(interaction: discord.Interaction):
        await interaction.response.send_message("balls indeed")