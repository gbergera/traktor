from graphs.plot_annotate_corners import plot_corner_graph
import discord
from discord.ext import commands
from discord import app_commands

def setup(client: commands.Bot):
    @client.tree.command(name="cornergraph", description="Show an image of a track's corners")
    @app_commands.describe(
        gp="The Grand Prix name (e.g. monza, bahrain, monaco)",
        year="The season year (e.g. 2024)"
    )
    async def cornergraph_command(interaction: discord.Interaction, year: int, gp: str):
        await interaction.response.defer()

        try:
            image_data = plot_corner_graph(year, gp)
            discord_file = discord.File(image_data, filename="track_map.png")

            embed = discord.Embed(
                title=f"{gp.title()} {year} - Track Corners",
                description="Track map with numbered corners",
                color=discord.Color.red()
            )
            embed.set_image(url="attachment://track_map.png")

            await interaction.followup.send(embed=embed, file=discord_file)

        except Exception as e:
            await interaction.followup.send(
                f"❌ Failed to generate map for `{gp}` {year}",
                ephemeral=True
            )
            print(e)
