import discord
from discord.ext import commands
from discord import app_commands
import f1requests.f1_requests as f1_requests

ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")

def setup(client: commands.Bot):
    @client.tree.command(name="gpresults", description="Show session results for a specific Grand Prix")
    @app_commands.describe(
        gp="The Grand Prix name (e.g. monza, monaco, bahrain)",
        year="The F1 season year (e.g. 2024)",
        session="The session type (e.g. qualifying, race)"
    )
    async def gp_session_embed(interaction: discord.Interaction, year: int, gp: str, session: str):
        try:
            await interaction.response.defer()

            session_clean = session.strip().lower()
            points_sessions = {"race", "r", "sprint", "s"}

            results = f1_requests.getGPSessionResult(year, gp, session_clean)

            if results is None or results.empty:
                await interaction.followup.send(
                    f"⚠️ No results found for {gp} {session} in {year}.", ephemeral=True
                )
                return

            ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")

            embed = discord.Embed(
                title=f"{gp.title()} {year} - {session.title()} Results",
                description=f"Positions at {gp.title()} in the {year} season",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url="attachment://TRUCK.png")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
            embed.set_footer(text="Traktor")

            # Add fields for each driver in results
            for idx, (_, row) in enumerate(results.iterrows(), start=1):
                abbreviation = str(row.get('Abbreviation', 'N/A'))
                status = str(row.get('Status', 'N/A'))

                if session_clean in points_sessions:
                    position = str(row.get('GridPosition', 'N/A'))
                    points = str(row.get('Points', '0'))
                    embed.add_field(
                        name=f"{idx} - {abbreviation}: {points} points",
                        value=f"Starting Position: {position} | Status: {status}",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"{idx}",
                        value=f"{abbreviation}",
                        inline=False
                    )

            await interaction.followup.send(embed=embed, file=ICON)

        except Exception as e:
            await interaction.followup.send("❌ Error: Could not fetch session results.", ephemeral=True)
            print(e)
