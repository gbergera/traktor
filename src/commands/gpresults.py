import discord
from discord.ext import commands
from discord import app_commands
import requests.f1_requests as f1_requests

ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="gpresults", description="Show session results for a specific Grand Prix")
    @app_commands.describe(gp="The Grand Prix name (e.g. monza, monaco, bahrain)", year="The F1 season year (e.g. 2024)", session="The session type (e.g. qualifying, race)")
    async def gp_session_embed(interaction: discord.Interaction, year: int, gp: str, session: str):
        try:
            await interaction.response.defer()  # Defer in case it takes a moment
    
            # Call the function to get the session results
            results = f1_requests.getGPSessionResult(year, gp, session)
    
            if results is None or results.empty:
                await interaction.followup.send(f"⚠️ No results found for {gp} {session} in {year}.", ephemeral=True)
                return
    
            ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")
    
            embed = discord.Embed(
                title=f"{gp} {year} - Results  ",
                description=f"Positions at {gp} in the {year} season",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="attachment://TRUCK.png")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text="F1 Results Tracker")
    
            # Add fields for the session results
            for index, row in results.iterrows():
                position = row['GridPosition']
                abbreviation = row['Abbreviation']
                points = row['Points']
                status = row['Status']
                embed.add_field(
                    name=f"Position {position}",
                    value=f"{abbreviation}: {points} points | Status: {status}",
                    inline=False
                )
    
            await interaction.followup.send(embed=embed, file=ICON)
    
        except Exception as e:
            await interaction.followup.send("❌ Error: Could not fetch session results.", ephemeral=True)
            print(e)