from graphs.plot_gear_shifts_on_track import plot_gear_shift_graph
import discord
from discord.ext import commands
from discord import app_commands
import io

def setup(client: commands.Bot):
    @client.tree.command(name="gearshifts", description="Visualize gear shifts on track for a session")
    @app_commands.describe(
        gp="The Grand Prix name (e.g. monza, bahrain, monaco)",
        year="The season year (e.g. 2021, 2024)",
        session="Session type (e.g. FP1/2/3, Q(Qualy), S(Sprint), R(Race))"
    )
    async def gearshifts_command(
        interaction: discord.Interaction,
        year: int,
        gp: str,
        session: str
    ):
        await interaction.response.defer()

        try:
            image_bytes = plot_gear_shift_graph(year, gp, session)
            discord_file = discord.File(fp=image_bytes, filename="gear_shift.png")

            embed = discord.Embed(
                title=f"{gp.title()} {year} - {session.upper()} Gear Shifts",
                description="Each color shows a different gear used around the track",
                color=discord.Color.orange()
            )
            embed.set_image(url="attachment://gear_shift.png")

            await interaction.followup.send(embed=embed, file=discord_file)

        except Exception as e:
            await interaction.followup.send(f"❌ Could not generate gear shift plot: {e}", ephemeral=True)
            print(e)
