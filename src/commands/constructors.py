import discord
from discord.ext import commands
from discord import app_commands
import requests.f1_requests as f1_requests

ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="constructors", description="Show constructor standings by year")
    @app_commands.describe(year="The season year to fetch standings from")
    async def constructor_standings_embed(interaction: discord.Interaction, year: int):
        try:
            standings = f1_requests.getConstructorStandings(year)
    
            ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")
    
            embed = discord.Embed(
                title=f"Constructor Standings - {year}",
                url="https://www.formula1.com/",
                description=f"F1 Constructors in {year}",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="attachment://TRUCK.png")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text="Traktor")
    
            embeds = [embed]
            current_embed = embed
    
            for _, row in standings.iterrows():
                field_title = f"**{row['positionText']}. {row['constructorName']}**"
                field_value = f"Points: {row['points']} | Wins: {row['wins']}\nNationality: {row['constructorNationality']}"
    
                if len(current_embed.fields) >= 25:
                    current_embed = discord.Embed(
                        title=f"Constructor Standings - {year} (cont.)",
                        color=discord.Color.red()
                    )
                    embeds.append(current_embed)
    
                current_embed.add_field(name=field_title, value=field_value, inline=False)
    
            await interaction.channel.send(embed=embeds[0], file=ICON)
    
            for e in embeds[1:]:
                await interaction.channel.send(embed=e)
    
            await interaction.response.send_message(f"Constructor standings for {year}:", ephemeral=False)
    
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: Could not fetch standings for year {year}.", ephemeral=True)
            print(e)
