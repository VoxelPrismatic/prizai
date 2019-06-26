#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from dyn import refresh
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify.embedify(desc=f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

def rext(name, bot): print(name); bot.reload_extension(name); print(f'>Rext {name}')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def rld(ctx, *name):
    allext, lodtxt = refresh.refresh()
    await log(ctx.bot, 'EXT', 'Reloading ext(s)')
    async with ctx.channel.typing():
        if not len(name):
            for ext in range(len(allext)):
                for com in allext[ext]: rext(f"{lodtxt[ext]}{com}", ctx.bot)
        else: rext(name[0], ctx.bot)
    await log(ctx.bot, 'EXT', 'ext(s) successfully reloaded')
    await ctx.message.add_reaction('👌')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rld)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rld')
    print('GOOD')

