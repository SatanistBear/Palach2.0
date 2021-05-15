import discord
from discord.ext import commands
import asyncio
import time
import dis_token
import re
import gym_db

bot = commands.Bot(command_prefix='-')

TOKEN = dis_token.discord_token()

gym_db.init()

@bot.event
async def on_ready():
    print("Бог качалки пробудился")


@bot.event
async def on_message(message):
    if message.author.id != 842356746604904448:  # Check if it's bot's message
        if re.search('г[ао]*ндо*н|г[ао]*рдо*н', message.content, flags=re.I):
            if gym_db.get_condoms(message.author.id) is None:
                gym_db.add_member(message.author.id)
                await message.channel.send('`Поздравляю с первым словом *гандон*, теперь ты ♂FUCKING SLAVE♂`')
            else:
                gym_db.add_condom(message.author.id)
                await message.channel.send('Кто сказал?')

        await bot.process_commands(message)


@bot.command(pass_context=True)
async def condom_ranking(ctx):
    all_condoms = gym_db.get_all_condoms()
    all_condoms.sort()
    print(all_condoms)
    ranking_board = '```\tТаблица лидеров по использованным гандонам:\n---------------\n'
    for tuple in all_condoms:
        member = await ctx.guild.fetch_member(tuple[0])
        name = member.name
        ranking_board += f'{name} - {tuple[1]} гандонов'
    ranking_board += '```'
        # ranking_board +=
    await ctx.send(ranking_board)


bot.run(TOKEN)
