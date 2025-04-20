import discord
from discord.ext import commands
from discord import app_commands
import f1requests.f1_requests as f1_requests

ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="gpinfo", description="Show detailed info for a specific Grand Prix")
    @app_commands.describe(gp="The Grand Prix name (e.g. monza, monaco, bahrain)",year="The F1 season year (e.g. 2024)")
    async def gp_info_embed(interaction: discord.Interaction, year: int, gp: str):
        try:
            await interaction.response.defer()  # Defer in case it takes a moment
    
            event_data = f1_requests.getGPInfoByName(gp, year)
    
            if event_data is None or event_data.empty:
                await interaction.followup.send(f"⚠️ GP '{gp}' not found for year {year}.", ephemeral=True)
                return
    
            ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")
    
            embed = discord.Embed(
                title=f"{event_data['EventName']} - {year}",
                description="Event Info from the F1 Schedule",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="attachment://TRUCK.png")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text="Traktor")
    
            embed.add_field(name="📍 Location", value=event_data["Location"], inline=True)
            embed.add_field(name="🏁 Round", value=str(event_data["RoundNumber"]), inline=True)
            embed.add_field(
                name="📅 Race Date",
                value=event_data["Session5DateUtc"].strftime('%A, %d %B %Y - %H:%M UTC'),
                inline=False
            )
    
            await interaction.followup.send(embed=embed, file=ICON)
    
        except Exception as e:
            await interaction.followup.send("❌ Error: Could not fetch GP info.", ephemeral=True)
            print(e)