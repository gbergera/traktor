import discord
from discord.ext import commands
from discord import app_commands
import requests.f1_requests as f1_requests

ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="seasonschedule",description="Show the full Grand Prix calendar for a given season")
    @app_commands.describe(year="The season year (e.g. 2025)")
    async def season_schedule_embed(interaction: discord.Interaction, year: int):
        try:
            await interaction.response.defer()
    
            schedule_data = f1_requests.getSchedule(year)
    
            if schedule_data.empty:
                await interaction.followup.send("🚫 No schedule found for that season.", ephemeral=True)
                return
    
            ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")
    
            embed = discord.Embed(
                title=f"F1 {year} Season Calendar",
                description="Here’s the full race schedule for the selected season:",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="attachment://TRUCK.png")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed.set_footer(text="Traktor")
    
            for i, row in schedule_data.iterrows():
                round_number = row["RoundNumber"]
                event_name = row["EventName"]
                country = row["Country"]
                date = row["Session5DateUtc"].strftime('%A, %d %B %Y')
    
                embed.add_field(
                    name=f"🏁 Round {round_number}: {event_name}",
                    value=f"🌍 {country} | 📅 {date}",
                    inline=False
                )
    
            await interaction.followup.send(embed=embed, file=ICON)
    
        except Exception as e:
            await interaction.followup.send("❌ Error: Could not fetch schedule.", ephemeral=True)
            print(e)