from graphs.plot_speed_on_track import plot_speed_on_track_graph
import discord
from discord.ext import commands
from discord import app_commands

def setup(client: commands.Bot):
    @client.tree.command(name="trackspeed", description="Visualize track speeds for a Grand Prix")
    @app_commands.describe(
        year="The season year (e.g. 2023)",
        gp="The Grand Prix name (e.g. monza, bahrain, monaco)",
        session="Session type (e.g. FP1, FP2, Q, R, S)",
        driver="Driver abbreviation (e.g. VER, HAM, LEC)"
    )
    async def trackspeed_command(
        interaction: discord.Interaction,
        year: int,
        gp: str,
        session: str,
        driver: str
    ):
        await interaction.response.defer()

        try:
            image_bytes = plot_speed_on_track_graph(year, gp, session, driver)
            discord_file = discord.File(fp=image_bytes, filename="track_speed.png")

            embed = discord.Embed(
                title=f"{gp.title()} {year} - {session.upper()} - {driver.upper()} Speed",
                description="Speed visualization over the track using the fastest lap",
                color=discord.Color.red()
            )
            embed.set_image(url="attachment://track_speed.png")

            await interaction.followup.send(embed=embed, file=discord_file)

        except Exception as e:
            await interaction.followup.send(f"❌ Could not generate track speed plot: {e}", ephemeral=True)
            print(e)
