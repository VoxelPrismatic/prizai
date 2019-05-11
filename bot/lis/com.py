#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
bot = commands.Bot(command_prefix=";]")

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)
async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs


##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def on_command_completion(ctx):
    await log(ctx.bot, 'COMMAND', f'''----
>  COM // {ctx.command}
> ARGS // {ctx.args[1:]}
> CHNL // {ctx.channel.name}
>  USR // {ctx.author}
>  GLD // {ctx.guild}''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    bot.add_listener(on_command_completion)
    print('GOOD')

def teardown(bot):
    print('-LIS')
    bot.remove_listener('on_command_completion')
    print('GOOD')
