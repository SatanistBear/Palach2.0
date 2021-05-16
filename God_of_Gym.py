import discord
from discord.ext import commands
import asyncio
import time
import dis_token
import re
import random
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
            if gym_db.Condoms().get_condoms(message.author.id) is None:  # if this is the first condom word
                gym_db.Condoms().add_member(message.author.id)
                await message.channel.send('`Поздравляю с первым словом *гандон*, теперь ты ♂FUCKING SLAVE♂`')
            else:
                gym_db.Condoms().add_condom(message.author.id)
                fact_id = random.randint(0, gym_db.Facts().facts_max_id())

                await message.channel.send('```Интересный факт о презервативах:\n' + gym_db.Facts().r_fact(fact_id) + '```')

        await bot.process_commands(message)


@bot.command(pass_context=True)
async def condom_ranking(ctx):
    all_condoms = gym_db.Condoms().get_all_condoms()
    all_condoms.sort()
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


# def add_fact(fact):
#     facts = gym_db.Facts()
#     facts.w_fact(fact)
#
#
# def delete_fact():
#     gym_db.Facts().del_fact(2)
#

# add_fact("""""")
# delete_fact()
# print(gym_db.Facts().facts_max_id())
bot.run(TOKEN)
