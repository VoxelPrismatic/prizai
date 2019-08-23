#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, random
import asyncio, json
from util import pages
from dyn.faces import faces
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from pprint import pprint as pp
def entry(lit,coms:list,lbl,mini) -> list:
    """
    >>> CREATES AN ENTRY IN THE HELP TABLE <<<
    LIT  [LIST] - The Pages
    COMS [LIST] - The Commands
    LBL  [STR ] - Command Label
    """
    if len(coms) > (10 if not mini else 20):
        x = 0
        for y in coms:
            if not x % (10 if not mini else 20):
                lit.append(f'#] {lbl} [{int(x/(10 if not mini else 20))+1}/{len(range(0,len(coms),10))}]\n')
            lit[-1] += y +'\n'
            x += 1
    else:
        lit.append(f'#] {lbl}\n'+'\n'.join(coms))
    return lit

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["helpmod","modhelp",'modhlep'],
                  help = 'inf',
                  brief = 'Brings up the mod help message',
                  usage = ';]helpmod',
                  description = '[NO ARGS FOR THIS COMMAND]')
async def hlepmod(ctx, mini = ""):
    mini = bool(mini)
    lit = []
    coms = {}
    cats = ['MOD']
    for cat in cats:
        coms[cat] = []
    for com in ctx.bot.commands:
        if not mini:
            com_desc = f'] "{com.usage}"\n>  {com.brief} '+random.choice(faces())
        else:
            com_desc = f'> {com.name}'
        try:
            if com.help not in ['mod']:
                continue
            coms[com.help.upper()].append(com_desc)
        except:
            pass

    replce = {'MOD':'MODERATOR'}
    for cat in coms:
        lit = entry(lit,coms[cat],replce[cat],mini)

    await pages.PageThis(ctx, lit, "COMMANDS LIST", f"""```diff
-] {'{?stuff}'} - Optional argument
-] To see mod commands, use "{json.load(open('json/prefixes.json'))[str(ctx.guild.id)] if isinstance(ctx.channel, discord.TextChannel) else ';]'}hlepmod"
-] To have a conversation, use "]<txt>" or "{'}<txt>'}"
-] Some of your data is stored, use "{json.load(open('json/prefixes.json'))[str(ctx.guild.id)] if isinstance(ctx.channel, discord.TextChannel) else ';]'}data" to see more```""")


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hlepmod)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlepmod')
    print('GOOD')