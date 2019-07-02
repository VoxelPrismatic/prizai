#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def md(ctx, mID: discord.Message):
    special = "*_~|"
    x = mID.content
    for y in special: x.replace(y,'\\'+y)
    await ctx.send(x)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(md)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('md')
    print('GOOD')
