import discord
from discord.ext import commands
import asyncio
import time
import dis_token
import re
import random
import gym_db
import youtube_dl
import subprocess

bot = commands.Bot(command_prefix='-')

TOKEN = dis_token.discord_token()

gym_db.init()

# ---------vMusic settingsv------------
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

cmd = ['ffmpeg']
out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename), data=data)


# ---------^Music settings^------------


@bot.event
async def on_ready():
    print("Бог качалки пробудился")


@bot.event
async def on_message(message):
    if message.author.id != 842356746604904448:  # Check if it's bot's message
        if re.search('г[ао]*ндо*н|г[ао]*рдо*н', message.content, flags=re.I):
            if gym_db.Condoms().get_condoms(message.author.id) is None:  # if this is the first condom word
                gym_db.Condoms().add_member(message.author.id)
                await message.channel.send('`Поздравляю с первым словом *гандон*, теперь ты ♂FUCKING SLAVE♂`')
            else:
                gym_db.Condoms().add_condom(message.author.id)
                fact_id = random.randint(0, gym_db.Facts().facts_max_id())

                await message.channel.send('```Интересный факт о гандонах:\n' + gym_db.Facts().r_fact(fact_id) + '```')

        await bot.process_commands(message)


@bot.command(pass_context=True, help='condom words ranking')
async def condom_ranking(ctx):
    all_condoms = gym_db.Condoms().get_all_condoms()
    all_condoms.sort(key=lambda x: x[1], reverse=True)
    # print(all_condoms)
    ranking_board = '```\tТаблица лидеров по использованным гандонам:\n---------------\n'
    for tuple in all_condoms:
        try:
            member = await ctx.guild.fetch_member(tuple[0])
            name = member.name
            ranking_board += f'{name} - {tuple[1]} гандонов\n'
        except discord.errors.NotFound:
            pass

    ranking_board += '```'
        # ranking_board +=
    await ctx.send(ranking_board)


# ---------------Music---------------


@bot.command(pass_context=True, help='Join voice channel')
async def join_gym(ctx):
    if not ctx.message.author.voice:
        await ctx.message.channel.send("Ты ещё не в качалке, дружище")
    else:
        await ctx.message.author.voice.channel.connect()



@bot.command(pass_context=True, help='Leave voice channel')
async def leave_gym(ctx):
    await ctx.message.guild.voice_client.disconnect()


@bot.command(pass_context=True, help='Play gachi remix (-gachi url)')
async def gachi(ctx, url):
    voice_client = ctx.message.guild.voice_client
    player = await YTDLSource.from_url(url, loop=bot.loop)
    voice_client.play(player, after=lambda e: print(f'Player error: {e}' if e else None))




bot.run(TOKEN)
