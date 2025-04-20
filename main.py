import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import f1_requests
from datetime import datetime



intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = discord.Object(id=int(os.getenv("DISCORD_SERVER_ID")))
ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")
#SOUNDS = {
#    "leclerc": "sounds/leclerc.mp3",
#    "max": "sounds/max.mp3",
#    "alonso": "sounds/alonso.mp3"
#}

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} commands.')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('traktor'):
            print(f'Message from {message.author}: {message.content}')
            await message.channel.send('balls')

client = Client(command_prefix="!", intents=intents)


@client.tree.command(name="balls", description="just do it")
async def say_balls(interaction: discord.Interaction):
    await interaction.response.send_message("balls indeed")

@client.tree.command(name="printer", description="copy message")
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

@client.tree.command(name="help", description="commands")
async def embed_demo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Traktor", url="https://www.formula1.com/", description="***🚜 Simply Lovely 🚜***", color=discord.Color.red()
    )
    embed.set_thumbnail(url="attachment://TRUCK.png")
    embed.add_field(name="🏎️ ***Balls*** 🏎️", value="balls", inline=True)
    embed.add_field(name="🏎️ ***Printer*** 🏎️", value="copy message ", inline=True)
    embed.add_field(name="🏎️ ***Drivers*** 🏎️", value="Show drivers standings", inline=False)
    embed.add_field(name="🏎️ ***Driverinfo*** 🏎️", value="Show driver info for a specific GP", inline=True)
    embed.add_field(name="🏎️ ***Constructors*** 🏎️", value="Show constructor standings", inline=True)
    embed.add_field(name="🏎️ ***Gpinfo*** 🏎️", value="Show detailed info for a specific Grand Prix", inline=False)
    embed.add_field(name="🏎️ ***Gpresults*** 🏎️", value="Show results of a specific Race", inline=True)
    embed.add_field(name="🏎️ ***Seasonschedule*** 🏎️", value="Show season schedule of a certain year", inline=True)
    embed.add_field(name="🏎️ ***Calendar*** 🏎️", value="Show calendar of the actual races", inline=False)
    embed.add_field(name="🏎️ ***Simplylovely*** 🏎️", value="Simply Lovely!", inline=True)
    embed.set_footer(text="Traktor")
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)

    await interaction.response.send_message(embed=embed, file=ICON)
    

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

        
@client.tree.command(name="drivers", description="Show driver standings by year")
@app_commands.describe(year="The season year to fetch standings from")
async def driver_standings_embed(interaction: discord.Interaction, year: int):
    try:
        standings = f1_requests.getDriverStandings(year)

        embed = discord.Embed(
            title=f"Driver Standings - {year}",
            url="https://www.formula1.com/",
            description=f"F1 Drivers in {year}",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="attachment://TRUCK.png")
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_footer(text="Traktor")

        embeds = [embed]
        current_embed = embed

        for i, row in standings.iterrows():
            field_title = f"**{row['position']}. {row['driverName']}**"
            field_value = (
                f"Points: {row['points']} | Wins: {row['wins']}\n"
                f"ID: `{row['driverCode']}` | Number: `{row['driverNumber']}`\n"
                f"Team(s): {', '.join(row['constructorIds']) if isinstance(row['constructorIds'], list) else row['constructorIds']}"
            )

            if len(current_embed.fields) >= 25:
                current_embed = discord.Embed(
                    title=f"Driver Standings - {year} (cont.)",
                    color=discord.Color.red()
                )
                embeds.append(current_embed)

            current_embed.add_field(name=field_title, value=field_value, inline=False)

        await interaction.channel.send(embed=embeds[0], file=ICON)

        for e in embeds[1:]:
            await interaction.channel.send(embed=e)

        await interaction.response.send_message(f"Driver standings for {year}:", ephemeral=False)

    except Exception as e:
        await interaction.response.send_message(f"❌ Error: Could not fetch driver standings for year {year}.", ephemeral=True)
        print(e)
        
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

@client.tree.command(name="calendar", description="Show the remaining Grand Prix races for the current season")
async def remaining_gp_embed(interaction: discord.Interaction):
    try:
        await interaction.response.defer()  # Defer to allow time for API call

        remaining = f1_requests.getRemainingGP()
        
        if remaining.empty:
            await interaction.followup.send("🏁 No remaining GPs found for this season!", ephemeral=True)
            return

        ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

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
        
@client.tree.command(name="gpinfo", description="Show detailed info for a specific Grand Prix")
@app_commands.describe(gp="The Grand Prix name (e.g. monza, monaco, bahrain)",year="The F1 season year (e.g. 2024)")
async def gp_info_embed(interaction: discord.Interaction, year: int, gp: str):
    try:
        await interaction.response.defer()  # Defer in case it takes a moment

        event_data = f1_requests.getGPInfoByName(gp, year)

        if event_data is None or event_data.empty:
            await interaction.followup.send(f"⚠️ GP '{gp}' not found for year {year}.", ephemeral=True)
            return

        ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

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
        

import discord
from discord import app_commands

@client.tree.command(name="gpresults", description="Show session results for a specific Grand Prix")
@app_commands.describe(gp="The Grand Prix name (e.g. monza, monaco, bahrain)", year="The F1 season year (e.g. 2024)", session="The session type (e.g. qualifying, race)")
async def gp_session_embed(interaction: discord.Interaction, year: int, gp: str, session: str):
    try:
        await interaction.response.defer()  # Defer in case it takes a moment

        # Call the function to get the session results
        results = f1_requests.getGPSessionResult(year, gp, session)

        if results is None or results.empty:
            await interaction.followup.send(f"⚠️ No results found for {gp} {session} in {year}.", ephemeral=True)
            return

        ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

        embed = discord.Embed(
            title=f"{gp} {year} - Results  ",
            description=f"Positions at {gp} in the {year} season",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="attachment://TRUCK.png")
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_footer(text="F1 Results Tracker")

        # Add fields for the session results
        for index, row in results.iterrows():
            position = row['GridPosition']
            abbreviation = row['Abbreviation']
            points = row['Points']
            status = row['Status']
            embed.add_field(
                name=f"Position {position}",
                value=f"{abbreviation}: {points} points | Status: {status}",
                inline=False
            )

        await interaction.followup.send(embed=embed, file=ICON)

    except Exception as e:
        await interaction.followup.send("❌ Error: Could not fetch session results.", ephemeral=True)
        print(e)

@client.tree.command(name="seasonschedule",description="Show the full Grand Prix calendar for a given season")
@app_commands.describe(year="The season year (e.g. 2025)")
async def season_schedule_embed(interaction: discord.Interaction, year: int):
    try:
        await interaction.response.defer()

        schedule_data = f1_requests.getSchedule(year)

        if schedule_data.empty:
            await interaction.followup.send("🚫 No schedule found for that season.", ephemeral=True)
            return

        ICON = discord.File("./img/TRUCK.png", filename="TRUCK.png")

        embed = discord.Embed(
            title=f"F1 {year} Season Calendar",
            description="Here’s the full race schedule for the selected season:",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="attachment://TRUCK.png")
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text="Traktor")

        for i, row in schedule_data.iterrows():
            round_number = row["RoundNumber"]
            event_name = row["EventName"]
            country = row["Country"]
            date = row["Session5DateUtc"].strftime('%A, %d %B %Y')

            embed.add_field(
                name=f"🏁 Round {round_number}: {event_name}",
                value=f"🌍 {country} | 📅 {date}",
                inline=False
            )

        await interaction.followup.send(embed=embed, file=ICON)

    except Exception as e:
        await interaction.followup.send("❌ Error: Could not fetch schedule.", ephemeral=True)
        print(e)

@client.tree.command(name="simplylovely", description="Simply Lovely!")
async def simply_lovely(interaction: discord.Interaction):
    try:
        await interaction.response.defer()

        image_path = "./img/SIMPLY LOVELY.png" 
        image_file = discord.File(image_path, filename="SIMPLY LOVELY.png")

        await interaction.followup.send(file=image_file)

    except Exception as e:
        await interaction.followup.send("❌ Error: Could not send the image.", ephemeral=True)
        print(e)

#TO DO: FINISH SOUNDBOARD COMMAND
#@client.tree.command(name='soundboard', description='Play a sound from the soundboard')
#@app_commands.describe(sound_name="Name of the sound to play")
#async def soundboard(interaction: discord.Interaction, sound_name: str):
#    if sound_name not in SOUNDS:
#        await interaction.response.send_message(
#            f"❌ Sound not found. Available: {', '.join(SOUNDS.keys())}", ephemeral=True
#        )
#        return
#
#    if not interaction.user.voice or not interaction.user.voice.channel:
#        await interaction.response.send_message("🚫 You must be in a voice channel to use this.", ephemeral=True)
#        return
#
#    await interaction.response.send_message(f"🔊 Playing `{sound_name}`...", ephemeral=False)
#
#    voice_channel = interaction.user.voice.channel
#    if interaction.guild.voice_client is None:
#        vc = await voice_channel.connect()
#    else:
#        vc = interaction.guild.voice_client
#        await vc.move_to(voice_channel)
#
#    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=SOUNDS[sound_name]))
#
#    while vc.is_playing():
#        await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=0.5))
#
#    await vc.disconnect()

client.run(TOKEN)
