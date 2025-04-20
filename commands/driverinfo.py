import discord
from discord.ext import commands
from discord import app_commands
import f1_requests

ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="driverinfo", description="Show driver info for a specific GP session")
    @app_commands.describe(gp="The Grand Prix name (e.g. monza, bahrain, monaco)",year="The season year (e.g. 2024)",session="Session type (e.g. FP1/2/3, Q(Qualy), S(Sprint), R(race))",driver_id="Driver ID (e.g. VER, HAM, NOR)")
    async def driver_info_embed(
        interaction: discord.Interaction,
        year: int,
        gp: str,
        session: str,
        driver_id: str
    ):
        try:
            await interaction.response.defer()  # only one response per interaction
    
            driver_df = f1_requests.getDriverInfoByGP(year, gp, session, driver_id)
            driver = driver_df.iloc[0]
    
            ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")
    
            embed = discord.Embed(
                title=f"{driver['FullName']} - {gp.title()} {year}",
                description=f"Performance in the **{gp.title()} GP**",
                color=discord.Color.red()
            )
    
            embed.set_thumbnail(url="attachment://TRUCK.png")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text="Traktor")
    
            embed.add_field(name="Team", value=driver["TeamName"], inline=True)
            embed.add_field(name="Abbreviation", value=driver["Abbreviation"], inline=True)
            embed.add_field(name="Number", value=driver["DriverNumber"], inline=True)
            embed.add_field(name="Country", value=driver["CountryCode"], inline=True)
            embed.add_field(name="Status", value=driver["Status"], inline=True)
            embed.add_field(name="Position", value=str(driver["Position"]), inline=True)
            embed.add_field(name="Points", value=str(driver["Points"]), inline=True)
    
            await interaction.followup.send(embed=embed, file=ICON)
    
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error: Could not fetch info for driver `{driver_id}` in {gp.title()} {year}.",
                ephemeral=True
            )
            print(e)