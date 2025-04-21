import discord
from discord.ext import commands
from discord import app_commands
import f1requests.f1_requests as f1_requests

ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="help", description="commands")
    async def embed(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Traktor", url="https://www.formula1.com/", description="***🚜 Simply Lovely 🚜***", color=discord.Color.red()
        )
        embed.set_thumbnail(url="attachment://TRUCK.png")
        embed.add_field(name="🏎️ ***Balls*** 🏎️", value="balls", inline=True)
        embed.add_field(name="🏎️ ***Printer*** 🏎️", value="copy message ", inline=True)
        embed.add_field(name="🏎️ ***Drivers*** 🏎️", value="Show drivers standings", inline=False)
        embed.add_field(name="🏎️ ***Driverinfo*** 🏎️", value="Show driver info for a specific GP", inline=True)
        embed.add_field(name="🏎️ ***Constructors*** 🏎️", value="Show constructor standings", inline=True)
        embed.add_field(name="🏎️ ***Gpinfo*** 🏎️", value="Show detailed info for a specific Grand Prix", inline=False)
        embed.add_field(name="🏎️ ***Gpresults*** 🏎️", value="Show results of a specific Race", inline=True)
        embed.add_field(name="🏎️ ***Seasonschedule*** 🏎️", value="Show season schedule of a certain year", inline=True)
        embed.add_field(name="🏎️ ***Calendar*** 🏎️", value="Show calendar of the actual races", inline=False)
        embed.add_field(name="🏎️ ***Trackspeed*** 🏎️", value="Shows an image of a specific driver in a session!", inline=True)
        embed.add_field(name="🏎️ ***Qualifyingresults*** 🏎️", value="Shows an image with the gap between each driver in qualy", inline=False)
        embed.add_field(name="🏎️ ***Cornergraph*** 🏎️", value="Shows an image of the different corners in a certain Grand Prix", inline=False)
        embed.add_field(name="🏎️ ***Positionchanges*** 🏎️", value="Shows an image of the position changes of the race", inline=True)
        embed.add_field(name="🏎️ ***Simplylovely*** 🏎️", value="Simply Lovely!", inline=False)
        
        embed.set_footer(text="Traktor")
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
    
        await interaction.response.send_message(embed=embed, file=ICON)