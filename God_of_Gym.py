import discord
from discord.ext import commands
import asyncio
import time
import dis_token
import re
import random
import gym_db
import games
# from pynput.keyboard import Key, Controller
# import pynput
# import pyautogui
# from win32gui import GetWindowText, GetForegroundWindow

bot = commands.Bot(command_prefix='-')

TOKEN = dis_token.discord_token()

gym_db.init()


@bot.event
async def on_ready():
    print("Бог качалки пробудился")
    i = 0
    while True:
        economy = gym_db.Economy()
        economy.update_currency()
        print("Валюты обновлены")
        if i >= 10:
            economy.hour_bucks()
            i = 0
        await asyncio.sleep(60)
        i += 1


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


@bot.command(pass_context=True, help='Shows your bank account')
async def bank(ctx):
    money_inf = gym_db.Economy().get_money_info(ctx.message.author.id)
    #gym_db.Economy().change_bucks(ctx.message.author.id, 270)
    await ctx.send(f"```На счету -{ctx.message.author.name}-\nBucks-ов: {money_inf[0]}\nТугриков: {money_inf[1]}\n"
                   f"Червонцев: {money_inf[2]}\nBondage-ей: {money_inf[3]}```")


@bot.command(pass_context=True, help='-casino [money] //You know what it is')
async def casino(ctx, money):
    money = float(money)
    result = games.casino(money)
    economy = gym_db.Economy()
    bank_money = economy.get_money_info(ctx.message.author.id)[0]
    print(money, result, bank_money)
    if bank_money - money > 0:
        economy.change_bucks(ctx.message.author.id, result)
        if result == money:
            await ctx.send(f"```Ты победил. Держи свои ♂{money} BUCKS♂\n"
                           f"~У тебя {bank_money + result} bucks на счету~```")
        elif result == -money:
            await ctx.send(f"```Ты проиграл мой ♂SLAVE♂, главное не ставь свой ♂ANAL♂ на кон\n"
                           f"~У тебя {bank_money + result} bucks на счету~```")
        elif result == money * 20:
            await ctx.send(f"```♂OHH, FUCK♂!!! Джекпот!!! Теперь ты настоящий ♂DANGEON MASTER♂\n"
                           f"~У тебя {bank_money + result} bucks на счету~```")
    else:
        await ctx.send("```Слишком большая сумма для тебя, мой ♂FUCKING SLAVE♂```")


@bot.command(pass_context=True, help='-casino [money] //You know what it is')
async def topbucks(ctx):
    top_info = gym_db.Economy().get_top_info()
    result = "```~Топ игроков по баксам~\n\n"
    i = 0
    for player in top_info:
        i += 1
        if i > 10:
            break
        try:
            member = await bot.fetch_user(player[0])  # member_id
            bucks = player[1]  # bucks
            result += f"{i}. {member.name} - {bucks} Bucks\n"
        except OverflowError:
            pass
    result += "```"
    await ctx.send(result)


@bot.command(pass_context=True, help='-currency //Показывает курс местных валют')
async def currency(ctx):
    economy = gym_db.Economy()
    # economy.rand_currency()
    currency_data = economy.get_currency()
    await ctx.send(f"```~Курсы валют на сейчас~\nЧервонцы - {currency_data[0][-1]}\n"
                   f"Тугрики - {currency_data[1][-1]}```", file=discord.File(economy.get_currency_graf()))
    await ctx.send(f"```~Курс Bondage~\nBondage - {currency_data[2][-1]}```",
                   file=discord.File(economy.get_bondage_graf()))


@bot.command(pass_context=True, help='-buy [name] [сумма в баксах] //Купить валют. c - Червонцы, t - Тугрики, b - Бондэйдж')
async def buy(ctx, curr, money):
    economy = gym_db.Economy()
    player_money = economy.get_money_info(ctx.message.author.id)
    currency = economy.get_currency()
    if float(money) <= player_money[0]:
        if curr.lower() == "t":
            economy.change_tug(ctx.message.author.id, float(money) / currency[0][-1])
            economy.change_bucks(ctx.message.author.id, -float(money))
            await ctx.send(f"```Ты купил {float(money) / currency[0][-1]} тугриков```")
        elif curr.lower() == "c":
            economy.change_cherv(ctx.message.author.id, float(money)/currency[1][-1])
            economy.change_bucks(ctx.message.author.id, -float(money))
            await ctx.send(f"```Ты купил {float(money) / currency[1][-1]} червонцев```")
        elif curr.lower() == "b":
            economy.change_bondage(ctx.message.author.id, float(money)/currency[2][-1])
            economy.change_bucks(ctx.message.author.id, -float(money))
            await ctx.send(f"```Ты купил {float(money) / currency[2][-1]} Bondage-ей```")
    else:
        await ctx.send("```Многовато для тебя, дружок-♂ANAL♂жок```")


@bot.command(pass_context=True, help='-sell [имя] [сумма] //Продать валют. c - Червонцы, t - Тугрики, b - Бондэйдж')
async def sell(ctx, curr, ammount):
    economy = gym_db.Economy()
    player_money = economy.get_money_info(ctx.message.author.id)
    currency = economy.get_currency()
    if curr.lower() == "t":
        if player_money[1] > float(ammount):
            economy.change_tug(ctx.message.author.id, -float(ammount))
            economy.change_bucks(ctx.message.author.id, float(ammount) * currency[0][-1])
            await ctx.send(f"```Ты успешно продал тугрики на {float(ammount) * currency[0][-1]} Bucks-ов```")
        else:
            await ctx.send("```Многовато для тебя, дружок-пирожок```")
    elif curr.lower() == "c":
        if player_money[2] > float(ammount):
            economy.change_cherv(ctx.message.author.id, -float(ammount))
            economy.change_bucks(ctx.message.author.id, float(ammount) * currency[1][-1])
            await ctx.send(f"```Ты успешно продал червонцы на {float(ammount) * currency[1][-1]} Bucks-ов```")
        else:
            await ctx.send("```Многовато для тебя, дружок-пирожок```")
    elif curr.lower() == "b":
        if player_money[3] > float(ammount):
            economy.change_bondage(ctx.message.author.id, -float(ammount))
            economy.change_bucks(ctx.message.author.id, float(ammount) * currency[2][-1])
            await ctx.send(f"```Ты успешно продал Bondage-и на {float(ammount) * currency[2][-1]} Bucks-ов```")
        else:
            await ctx.send("```Многовато для тебя, дружок-пирожок```")


# ----------------------Remote-Control----------------------------
# keyboard = Controller()
# mouse = pynput.mouse.Controller()
# holded = []
#
#
# def check_terraria():
#     win = GetWindowText(GetForegroundWindow())
#     if win.find("Terraria") == 0:
#         return True
#     else:
#         return False
#
#
# def face_control(ctx):
#     if ctx.message.author.id == 272649817866633217 or \
#             (ctx.message.author.id == 296506452800176128 and check_terraria()):
#         return True
#     else:
#         return False
#
#
# @bot.command(pass_context=True, help='-p [key name] [time in secs] '
#                                      '//Pressing the key for some time ("left" and "right" for mouse clicks)')
# async def p(ctx, key, time):
#     if face_control(ctx):
#         if key.lower() == "space":
#             with keyboard.pressed(Key.space):
#                 await ctx.send("Клавиша зажата")
#                 await asyncio.sleep(float(time))
#         elif key.lower() == "enter":
#             with keyboard.pressed(Key.enter):
#                 await ctx.send("Клавиша зажата")
#                 await asyncio.sleep(float(time))
#         elif key.lower() == "left":
#             await ctx.send("Клавиша зажата")
#             mouse.press(pynput.mouse.Button.left)
#             await asyncio.sleep(float(time))
#             mouse.release(pynput.mouse.Button.left)
#         elif key.lower() == "right":
#             await ctx.send("Клавиша зажата")
#             mouse.press(pynput.mouse.Button.right)
#             await asyncio.sleep(float(time))
#             mouse.release(pynput.mouse.Button.right)
#         elif key.lower() == "esc":
#             await ctx.send("Клавиша зажата")
#             with keyboard.pressed(Key.esc):
#                 await asyncio.sleep(float(time))
#         else:
#             await ctx.send("Клавиша зажата")
#             with keyboard.pressed(key):
#                 await asyncio.sleep(float(time))
#         await ctx.send("Клавиша отжата")
#     else:
#         await ctx.send("Обойдёшься")
#
#
# @bot.command(pass_context=True, help='-hold [key name]//Holding the key while not released')
# async def hold(ctx, key):
#     if face_control(ctx):
#         if key.lower() == "space":
#             keyboard.press(Key.space)
#             await ctx.send("Клавиша зажата")
#             holded.append(key)
#         elif key.lower() == "enter":
#             keyboard.press(Key.enter)
#             await ctx.send("Клавиша зажата")
#             holded.append(key)
#         elif key.lower() == "left":
#             await ctx.send("Клавиша зажата")
#             mouse.press(pynput.mouse.Button.left)
#             holded.append(key)
#         elif key.lower() == "right":
#             await ctx.send("Клавиша зажата")
#             mouse.press(pynput.mouse.Button.right)
#             holded.append(key)
#         elif key.lower() == "esc":
#             await ctx.send("Клавиша зажата")
#             keyboard.press(Key.esc)
#             holded.append(key)
#         else:
#             await ctx.send("Клавиша зажата")
#             keyboard.press(key)
#             holded.append(key)
#     else:
#         await ctx.send("Обойдёшься")
#
#
# @bot.command(pass_context=True, help='-release [key name]//Releasing the key')
# async def release(ctx, key):
#     if face_control(ctx):
#         if key.lower() == "space":
#             keyboard.release(Key.space)
#
#             try:
#                 holded.remove(key)
#                 await ctx.send("Клавиша отжата")
#             except Exception:
#                 await ctx.send("Но она и не была зажата")
#         elif key.lower() == "enter":
#             keyboard.release(Key.enter)
#
#             try:
#                 holded.remove(key)
#                 await ctx.send("Клавиша отжата")
#             except Exception:
#                 await ctx.send("Но она и не была зажата")
#
#         elif key.lower() == "left":
#             await ctx.send("Клавиша отжата")
#             mouse.release(pynput.mouse.Button.left)
#
#             try:
#                 holded.remove(key)
#                 await ctx.send("Клавиша отжата")
#             except Exception:
#                 await ctx.send("Но она и не была зажата")
#
#         elif key.lower() == "right":
#             mouse.release(pynput.mouse.Button.right)
#             try:
#                 holded.remove(key)
#                 await ctx.send("Клавиша отжата")
#             except Exception:
#                 await ctx.send("Но она и не была зажата")
#
#         elif key.lower() == "esc":
#             keyboard.release(Key.esc)
#
#             try:
#                 holded.remove(key)
#                 await ctx.send("Клавиша отжата")
#             except Exception:
#                 await ctx.send("Но она и не была зажата")
#
#         else:
#             keyboard.release(key)
#             try:
#                 holded.remove(key)
#                 await ctx.send("Клавиша отжата")
#             except Exception:
#                 await ctx.send("Но она и не была зажата")
#     else:
#         await ctx.send("Обойдёшься")
#
#
# @bot.command(pass_context=True, help='-screen // Making screenshot')
# async def screen(ctx):
#     if face_control(ctx):
#         screen = pyautogui.screenshot()
#         screen.save("screen.png")
#         await ctx.send("На", file=discord.File("screen.png"))
#     else:
#         await ctx.send("Обойдёшься")
#
#
# @bot.command(pass_context=True, help='-m_pos [x] [y] // Moving mouse (x < 1080; y < 1920). (0;0) - up left corner.')
# async def m_pos(ctx, x, y):
#     if face_control(ctx):
#         x = int(x)
#         y = int(y)
#         if 0 < x < 1920 and 0 < y < 1080:
#             pyautogui.moveTo(x, y)
#         await ctx.send("Мышь передвинута")
#     else:
#         await ctx.send("Обойдёшься")



bot.run(TOKEN)
