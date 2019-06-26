#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
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
async def coin(ctx, *nums: int):
        lit = []
        if len(nums) == 0: num = 1
        else: num = int(nums[0])
        tcnt = y = hcnt = 0
        outp = ""
        if num > 5000:
            await ctx.send('```]To prevent spam, MAX = 5000```')
            num = 5000
        for x in range(num):
            if rand(0,1): tcnt+=1; outp = outp+"[T] "
            else: hcnt+=1; outp = outp+"[H] "
            if y == 200:
                lit.append(str(outp))
                outp = ""; y = 0
            else: y+=1
        if y != 0: lit.append(str(outp))
        await pages.PageThis(ctx, lit, "COINS", low=f'```]HEAD // {hcnt}\n]TAIL // {tcnt}```')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(coin)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('coin')
    print('GOOD')

