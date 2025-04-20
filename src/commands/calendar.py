import discord
from discord.ext import commands
from discord import app_commands
import f1requests.f1_requests as f1_requests
from datetime import datetime

ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="calendar", description="Show the remaining Grand Prix races for the current season")
    async def remaining_gp_embed(interaction: discord.Interaction):
        try:
            await interaction.response.defer()  # Defer to allow time for API call
    
            remaining = f1_requests.getRemainingGP()
            
            if remaining.empty:
                await interaction.followup.send("🏁 No remaining GPs found for this season!", ephemeral=True)
                return
    
            ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")
    
            embed = discord.Embed(
                title=f"Remaining GPs - {datetime.now().year}",
                description="Here are the upcoming Formula 1 races:",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="attachment://TRUCK.png")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text="Traktor")
    
            # Add each remaining GP
            for i, row in remaining.iterrows():
                gp_title = f"🏎️ {row['EventName']} - {row['Location']}"
                gp_date = row['Session5DateUtc'].strftime('%A, %d %B %Y - %H:%M UTC')
                embed.add_field(name=gp_title, value=f"📅 {gp_date}", inline=False)
    
            await interaction.followup.send(embed=embed, file=ICON)
    
        except Exception as e:
            await interaction.followup.send("❌ Error: Could not fetch remaining GPs.", ephemeral=True)
            print(e)