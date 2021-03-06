import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
import datetime
from util.embedify import emb
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

def init():
    global _inst
    _inst = dict()

async def PageThis(ctx, lit, name, low = "", thumb = None, mono = True, typ = 'md'):
    """
    >>> MAIN PAGINATOR FOR MOST COMMANDS <<<
      CTX - [CTX ] Context, allows this paginator to grab the author, channel, and other things
      LIT - [LIST] Pages in the form of a list, easy paging
      LOW - [STR ] Footer, on every page, none by default
      TYP - [STR ] Sets the monospace syntax highlighting, MarkDown by default
     NAME - [STR ] Title text
     MONO - [STR ] Sets the input text to monospace, on by default
    THUMB - [STR ] Link to thumbnail to an **IMAGE** [only http[s] supported], None by default
    """
    bot = ctx.bot
    num = 0
    usr = ctx.author

    def check(reaction, user):
        """
        CHECKS IF THE REACTION AUTHOR IS THE SAME AS THE PERSON WHO
        INVOKED THE COMMAND
        """
        try: return user == _inst[reaction.message.id]['usr']
        except: pass

    def save(msg, lit, num, usr, low, name, thumb, mono, typ):
        """
        >>> SAVES THE CONTENTS TO A DICT <<<
      CTX - [CTX ] Context, allows this paginator to grab the author, channel, and other things
      LIT - [LIST] Pages in the form of a list, easy paging
      LOW - [STR ] Footer, on every page, none by default
      TYP - [STR ] Sets the monospace syntax highlighting, MarkDown by default
      NUM - [INT ] The location
     NAME - [STR ] Title text
     MONO - [STR ] Sets the input text to monospace, on by default
    THUMB - [STR ] Link to thumbnail to an **IMAGE** [only http[s] supported], None by default
        """
        _inst[msg.id]={
            'msg':msg,  #Message Instance
            'lit':lit,  #Pages in list
            'num':num,  #Page Number
            'usr':usr,  #Author Instance
            'end':low,  #Footer
            'nam':name, #Header
            'img':thumb,#Thumbnail
            'mono':mono,#Is Monospace?
            'typ':typ
        }  #Monospace Syntax Highlighting
    #to get these emojis please let your bot join https://discord.gg/eYMyfcd
    _sL = '<:sl:598301530667483137>'
    _aL = '<:al:598301447066484747>'
    _stp = '<:stp:598301603069689876>'
    _aR = '<:ar:598301483645141003>'
    _sR = '<:sr:598301570387542036>'
    _num = '<:num:598301671642234919>'
    _del = '<:del:598301635718152241>'
    
    async def react(msg):
        "ADDS REACTIONS"
        for rct in r:
            await msg.add_reaction(rct)
        return msg

    def page(mID):
        """
        >>> CREATES A PAGE <<<
        mID - [INT] The message ID
        """
        itm = _inst[mID]
        return f"```md\n#] PRIZM {itm['nam']} ;]```" + \
               ('```' + itm['typ'] + '\n' if itm['mono'] else '') +\
               itm['lit'][itm['num']] +\
               ('```' if itm['mono'] else '\n') +\
               itm['end']

    if [list(foo.values())[3] for foo in _inst.values()].count(ctx.author) > 2:
        return await ctx.send('''```md
#] TOO MANY INSTANCES
>  You already have 3 commands open
>  Please close one to continue
>  This helps prevent spam :D```''')

    if len(lit) == 1:
        return await ctx.send(
            embed=emb(
                desc=f"```md\n#] PRIZM {name} ;]```" + ('```'+typ+'\n' if mono else '')\
                     + lit[num] + ('```' if mono else '\n')+low,
                foot=f"[1/{len(lit)}] // PRIZM ;]",
                thumb=thumb
            )
        )
    if len(lit) <= 3:
        r = [_aL, _stp, _aR, _del]
    elif len(lit) <= 5:
        r = [_aL, _stp, _aR, _num, _del]
    else:
        r = [_sL, _aL, _stp, _aR, _sR, _num, _del]
    msg = await react(
        await ctx.send(
            embed=emb(
                title='LOADING ;]',
                desc='```md\n#] STARTING... JUST A SEC```'
            )
        )
    )

    await msg.edit(
        embed=emb(
            desc=f"```md\n#] PRIZM {name} ;]```" + ('```'+typ+'\n' if mono else '')\
                 + lit[num] + ('```' if mono else '\n') + low,
            foot=f"[1/{len(lit)}] // PRIZM ;]",
            thumb=thumb
        )
    )

    if len(lit) > 1 and msg.id not in _inst:
        save(msg,lit,num,usr,low,name,thumb,mono,typ)
        while len(_inst) > 0:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                delet = []
                for tmsg in list(_inst)[:]:
                    imsg=_inst[tmsg]["msg"]
                    if imsg.edited_at is None:
                        tm = imsg.created_at.timestamp()
                    else:
                        tm = imsg.edited_at.timestamp()
                    if float(datetime.datetime.utcnow().timestamp()-tm) > 59:
                        delet.append(tmsg)
                        await imsg.edit(
                            embed=emb(
                                desc=page(imsg.id),
                                foot=f"[{num+1}/{len(lit)}] // TIMEOUT", 
                                thumb=thumb
                            )
                        )
                        try:
                            await imsg.clear_reactions()
                        except:
                            pass
                for m in delet:
                    del _inst[m]
            else:
                if reaction.message.id in _inst:
                    msg, lit, num, usr, low, name, thumb, mono, typ = _inst[reaction.message.id].values()
                    e = reaction.emoji
                    s = f'<:{e.name}:{e.id}>'

                    if s == _sL: #Skip Left
                        num = 0

                    elif s == _aL: #Arrow Left
                        num -= 1

                    elif s == _stp: #Stop
                        await msg.edit(
                            embed=emb(
                                desc=page(msg.id), 
                                foot=f"[{num+1}/{len(lit)}] // STOPPED", 
                                thumb=thumb
                            )
                        )
                        try:
                            await msg.clear_reactions()
                        except:
                            pass
                        try:
                            del _inst[reaction.message.id]
                        except:
                            pass
                        return

                    elif s == _del: #Recycle
                        del _inst[reaction.message.id]
                        return await msg.delete()

                    elif s == _aR: #Arrow Right
                        num += 1

                    elif s == _sR: #Skip Right
                        num = len(lit) - 1

                    elif s == _num: #Numbers
                        ms = await ctx.send('```md\n#] ENTER PAGE NUMBER```')
                        def chk(ms1):
                            return ms1.author == user
                        try:
                            ms1 = await bot.wait_for('message', timeout=10.0, check=chk)
                        except asyncio.TimeoutError:
                            await ms.delete()
                            await ctx.send('```diff\n-] TIMEOUT [10s]```', delete_after=5.0)
                        else:
                            try:
                                await ms.delete()
                                await ms1.delete()
                            except:
                                pass
                            try:
                                num = int(ms1.content)-1
                            except:
                                await ctx.send('```diff\n-] INVALID RESPONSE```', delete_after=5.0)

                    if num < 0:
                        num = len(lit) - 1

                    elif num > (len(lit) - 1):
                        num = 0

                    try:
                        await msg.remove_reaction(reaction, usr)
                        o = "PRIZM ;]"
                    except:
                        o = "PLEASE RE-REACT // PRIZM ;]"

                    save(msg, lit, num, usr, low, name, thumb, mono, typ)

                    await msg.edit(
                        embed=emb(
                            desc=page(msg.id),
                            foot=f'[{num+1}/{len(lit)}] // ' + o,
                            thumb=thumb
                        )
                    )