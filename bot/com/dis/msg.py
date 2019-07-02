#!/emj/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import pages
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
async def msg(ctx, _msg:discord.Message):
    try:
        lit = [f"""
     ID // {_msg.id}
    TTS // {_msg.tts}
    URL // [[LINK]](_msg.jump_url)
   USER // {_msg.author}
   CHNL // {_msg.channel}
 PINNED // {_msg.pinned}
 EDITED // {_msg.edited_at}
CREATED // {_msg.created_at}""", f"""
MENTION //
> USER ] {', '.join([mbr.name for mbr in _msg.mentions])}
> CHNL ] {', '.join([cnl.name for cnl in _msg.channel_mentions])}
> ROLE ] {', '.join([cnl.name for cnl in _msg.role_mentions])}
"""]
        if len(_msg.reactions) > 0:
            for r in _msg.reactions:
                usrs = await r.users().flatten()
                lit.append(f"REACTIONS [{r.emoji.name if r.custom_emoji else r.emoji}] // \n{', '.join(usr.name for usr in usrs)}")
        await pages.PageThis(ctx, lit, "MESSAGE INFO")
    except discord.HTTPException: await exc(ctx, 1)
    except discord.Forbidden: await exc(ctx, 2)
    except discord.NotFound: await exc(ctx, 3)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(msg)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('msg')
    print('GOOD')
