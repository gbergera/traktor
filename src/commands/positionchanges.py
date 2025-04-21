from graphs.plot_position_changes import plot_position_changes_graph
import discord
from discord.ext import commands
from discord import app_commands
import io

def setup(client: commands.Bot):
    @client.tree.command(name="positionchanges", description="Visualize position changes for a session")
    @app_commands.describe(
        year="The season year (e.g. 2023)",
        gp="The Grand Prix name (e.g. monza, bahrain, monaco)",
        session="Session type (e.g. FP1/2/3, Q(Qualy), S(Sprint), R(Race))"
    )
    async def positionchanges_command(
        interaction: discord.Interaction,
        year: int,
        gp: str,
        session: str
    ):
        await interaction.response.defer()

        try:
            image_bytes = plot_position_changes_graph(year, gp, session)
            discord_file = discord.File(fp=image_bytes, filename="position_changes.png")

            embed = discord.Embed(
                title=f"{gp.title()} {year} - {session.upper()} Position Changes",
                description="Driver positions at the end of each lap",
                color=discord.Color.blue()
            )
            embed.set_image(url="attachment://position_changes.png")

            await interaction.followup.send(embed=embed, file=discord_file)

        except Exception as e:
            await interaction.followup.send(f"❌ Could not generate position change plot: {e}", ephemeral=True)
            print(e)
