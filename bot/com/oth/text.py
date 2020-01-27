#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging, random, asyncio, time
import re
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot.logic import LogicAdapter



# Create a new instance of a ChatBot
cbot = ChatBot(
    'PRIZM ;]',
    storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
    logic_adapters = [
        {
            'import_path': 'chatterbot.logic.BestMatch'
        }
    ]
)

trainer = ChatterBotCorpusTrainer(cbot)

last = {}

chars = {
    "ŵ": "w",
    "èéêëēėę": "e",
    "ŷÿ": "y",
    "ūúùüû": "u",
    "ìįīíïî": "i",
    "õōøœóòöô": "o",
    "ªąāåãæäâáà": "a",
    "šśß": "s",
    "ł": "l",
    "żźž": "z",
    "čćç": "c",
    "ńñ": "n",
    "\u2019\u2018": "'",
    "\u201c\u201d": '"',
}

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = ['ai', 'chat', ''],
    help = 'ai',
    brief = 'You can have a conversation with me!',
    usage = ';]text {convo}',
    description = '''\
CONVO [TEXT] - The conversation
''')
@commands.check(enbl)
async def text(ctx, *, convo):
    global last
    if re.search(r"<:\w+:\d+>", convo):
        return await ctx.send("```diff\n-] I DON'T UNDERSTAND CUSTOM EMOJIS```")
    if not re.search(r"^[\d\w `~!@#$%^&*()-_=+\[\]{}\\|;:'\",<.>/?\n]+$", convo):
        return await ctx.send("```diff\n-] PLEASE USE ASCII ONLY```")
    async with ctx.channel.typing():
        convo = re.sub(r" +", r" ", convo)
        for r in chars:
            convo = re.sub("[" + "\\".join(r) + "]", chars[r], convo)
        response = cbot.get_response(convo)
    await ctx.send(response)
    if ctx.author in last and time.monotonic() - last[ctx.author][1] < 180:
        trainer = ListTrainer(cbot)
        trainer.train([last[ctx.author][0], convo])
    last[ctx.author] = [str(response), time.monotonic()]

@commands.command(help='ai',
                  brief='You can help me learn!',
                  usage=';]learn {?text}',
                  description='''\
TEXT [TEXT] - Preset conversation, each message on new line
''')
@commands.check(enbl)
async def learn(ctx, *, text:str = ""):
    trainer = ListTrainer(cbot)
    if text and '--corpus' in text:
        trainer = ChatterBotCorpusTrainer(cbot)
        for corpus in text.replace('--corpus','').splitlines():
            async with ctx.channel.typing():
                trainer.train(corpus.strip())
        return await ctx.send('```md\n#] THANKS!```')
    elif text:
        if len(''.join(text).splitlines()) % 2 != 1:
            async with ctx.channel.typing():
                trainer.train(''.join(text).splitlines())
            return await ctx.send('```md\n#] THANKS!```')
        else:
            return await ctx.send(
                '```diff\n-] MUST BE A FULL CONVERSATION'
                ' - AN EVEN AMOUNT OF MESSAGES```'
            )
    await ctx.send('''```md
#] YOU ARE ALLOWING ME TO STORE SOME DATA
>  This data is not identifiable, it is just
>  what you tell me to learn, I will learn
>  from the next 20 messages sent in this
>  channel, I hope you understand.```''')
    def check(msg):
        return msg.channel == ctx.channel
    learn = []
    for x in range(10):
        try:
            msg1 = await ctx.bot.wait_for(
                'message', timeout = 30.0, check = check
            )
            msg2 = await ctx.bot.wait_for(
                'message', timeout = 30.0, check = check
            )
        except asyncio.TimeoutError:
            async with ctx.channel.typing():
                if len(learn):
                    trainer.train(learn)
            return await ctx.send(
                '```diff\n-] 30 SEC SINCE LAST MESSAGE, TIMEOUT```'
            )
        else:
            if not random.randint(0,3):
                await ctx.send(random.choice(
                    [
                        'Ah, I get it',
                        'I see how this is going',
                        'mhm',
                        'makes sense',
                        'so thats how that works',
                        'yup',
                        'yeah ok.',
                        'now i understand'
                    ]
                ))
            learn.extend([msg1.content, msg2.content])
    async with ctx.channel.typing():
        trainer.train(learn)
    await ctx.send('```md\n#] THANKS FOR HELPING ME OUT!```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(text)
    bot.add_command(learn)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('text')
    bot.remove_command('learn')
    print('GOOD')
