import discord
from discord.ext import commands
from discord import app_commands
import f1requests.f1_requests as f1_requests


#ICON = discord.File("../img/TRUCK.png", filename="TRUCK.png")
#SOUNDS = {
#    "leclerc": "sounds/leclerc.mp3",
#    "max": "sounds/max.mp3",
#    "alonso": "sounds/alonso.mp3"
#}

#TO DO: FINISH SOUNDBOARD COMMAND
#def setup(client: commands.Bot):
#   @client.tree.command(name='soundboard', description='Play a sound from the soundboard')
#   @app_commands.describe(sound_name="Name of the sound to play")
#   async def soundboard(interaction: discord.Interaction, sound_name: str):
#       if sound_name not in SOUNDS:
#           await interaction.response.send_message(
#               f"❌ Sound not found. Available: {', '.join(SOUNDS.keys())}", ephemeral=True
#           )
#           return
#   
#       if not interaction.user.voice or not interaction.user.voice.channel:
#           await interaction.response.send_message("🚫 You must be in a voice channel to use this.", ephemeral=True)
#           return
#   
#       await interaction.response.send_message(f"🔊 Playing `{sound_name}`...", ephemeral=False)
#   
#       voice_channel = interaction.user.voice.channel
#       if interaction.guild.voice_client is None:
#           vc = await voice_channel.connect()
#       else:
#           vc = interaction.guild.voice_client
#           await vc.move_to(voice_channel)
#   
#       vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=SOUNDS[sound_name]))
#   
#       while vc.is_playing():
#           await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=0.5))
#   
#       await vc.disconnect()