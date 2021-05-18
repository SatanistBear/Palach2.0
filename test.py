import discord
from discord.ext import commands
import youtube_dl
import ctypes
import ctypes.util

Token = "XXXXXX" #your token         
client = commands.Bot(command_prefix = ":") 

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   

def endSong(guild, path):
    os.remove(path)

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" #link to your song on YouTube
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    file = ydl.extract_info(url, download=True)
    guild = "1234567890" #id of your server which you can get by right clicking on server name and clicking "Copy ID" (developer mode must be on)
    path = str(file['title']) + "-" + str(file['id'] + ".mp3")

channel1 = client.get_channel(1234567890) #id of your channel (you get it like server id, but by right clicking on channel)                         
voice_client = await channel1.connect()                                           

voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
    
while voice_client.is_playing(): #waits until song ends
    await asyncio.sleep(1)
else:
    await voice_client.disconnect() #and disconnects
    print("Disconnected")
