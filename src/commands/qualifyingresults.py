from graphs.plot_qualifying_results import plot_qualifying_results_graph
import discord
from discord.ext import commands
from discord import app_commands

def setup(client: commands.Bot):
    @client.tree.command(name="qualifyingresults", description="Visualize qualy results for a Grand Prix")
    @app_commands.describe(
        year="The season year (e.g. 2023)",
        gp="The Grand Prix name (e.g. monza, bahrain, monaco)",
    )
    async def qualifyingresults_command(
        interaction: discord.Interaction,
        year: int,
        gp: str,
    ):
        await interaction.response.defer()

        try:
            image_bytes = plot_qualifying_results_graph(year, gp)
            discord_file = discord.File(fp=image_bytes, filename="qualifying_results.png")

            embed = discord.Embed(
                title=f"{gp.title()} {year} - Qualifying Results",
                description="Fastest lap deltas relative to pole position",
                color=discord.Color.gold()
            )
            embed.set_image(url="attachment://qualifying_results.png")

            await interaction.followup.send(embed=embed, file=discord_file)

        except Exception as e:
            await interaction.followup.send(f"❌ Could not generate qualifying results plot: {e}", ephemeral=True)
            print(e)
