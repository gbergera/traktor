import discord
from discord.ext import commands
from discord import app_commands
import f1_requests

ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="simplylovely", description="Simply Lovely!")
    async def simply_lovely(interaction: discord.Interaction):
        try:
            await interaction.response.defer()
    
            image_path = "./img/SIMPLY LOVELY.png" 
            image_file = discord.File(image_path, filename="SIMPLY LOVELY.png")
    
            await interaction.followup.send(file=image_file)
    
        except Exception as e:
            await interaction.followup.send("❌ Error: Could not send the image.", ephemeral=True)
            print(e)