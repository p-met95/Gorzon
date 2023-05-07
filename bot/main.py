import os
print(os.getcwd())

import discord
from discord.ext import commands
from wordsearch import *
from fortune_cookie_generator import *
import datetime
import asyncio
import typing
from english_words import get_english_words_set

words = get_english_words_set(['web2'], alpha=True, lower=True)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!",intents=intents)
token = os.getenv("DISCORD_BOT_TOKEN")


numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
           "6⃣", "7⃣", "8⃣", "9⃣", "🔟")


print(os.getcwd())

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("I AM RISEN, BOW BEFORE ME"))
    print("I am online")
    # print('starting reminders')
    # what_ya_reading.start()
    # dnd_remind.start()


# reminder commands- REFACTOR soon, class? add create your own reminder?

# @tasks.loop(hours=24*7)
# async def what_ya_reading():
#    wid = 774654613894463509
#    ch = client.get_channel(762730040487313488)
#    await ch.send(f'Filthy <@&{wid}>, what degenerecy have you been reading/watching this week?')

# @what_ya_reading.before_loop
# async def before_reading():
#    for _ in range(60*60*24):  # loop the whole day
#        if datetime.datetime.now().hour - 5 == 4 + 12 and datetime.datetime.now().weekday() == 4:  # friday(4) @ 11am
#            print('pinging weebs')
#            return
#        await asyncio.sleep(1) # wait a second before looping again. You can make it more


# @tasks.loop(hours=24*7)
# async def dnd_remind():
#    wid = 570382098121097226
#    ch = client.get_channel(761387745863925762)
#    await ch.send(f'Feeble <@&{wid}>, session starts at 7:00pm EST.')

# @dnd_remind.before_loop
# async def before_dnd():
#    for _ in range(60*60*24):  # loop the whole day
#        if datetime.datetime.now().hour - 5 == 4 + 12 and datetime.datetime.now().weekday() == 2:  # wednesday (2) @ 4pm
#            print('pinging party')
#            return
#        await asyncio.sleep(1) # wait a second before looping again. You can make it more


###

@client.command()
async def sfws(ctx):
    """Posts 3 Safe For Work Sasuke™ for when you need to move that shit off screen."""
    await ctx.channel.send(file=discord.File('/bot/Images/sfwsasuke.png'))
    await ctx.channel.send(file=discord.File('/bot/Images/sfwsasuke.png'))
    await ctx.channel.send(file=discord.File('/bot/Images/sfwsasuke.png'))


# poll commands

@client.command(name='createpoll', aliases=['mkpoll'])
async def create_poll(ctx, question, polltime: typing.Optional[int] = 10, *options):
    """
    Create a poll, format as below:
    !mkpoll "This is the question?" 5 option1 "option two" option3
        - Default 10 minute poll time can be offset by adding
          in time (in minutes) after the question.
        - Options will be separated by space unless in quotes
    """

    if len(options) > 10:
        await ctx.channel.send('You can only have a max of 10 options.')

    embed = discord.Embed(title="Poll",
                          description=question,
                          colour=ctx.author.colour,
                          timestamp=datetime.datetime.utcnow())

    fields = [('Options', '\n'.join([f'{numbers[idx]} {option}' for idx, option in enumerate(options)]), False),
              ('Instructions:', 'React to cast a vote!', False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    message = await ctx.channel.send(embed=embed)
    cache_msg = discord.utils.get(client.cached_messages, id=message.id)

    for emoji in numbers[:len(options)]:
        await message.add_reaction(emoji)

    await asyncio.sleep(polltime * 60)

    allrxn = []

    for react in cache_msg.reactions:
        allrxn.append(react.count)

    allrxn = allrxn[:len(options)]

    m = max(allrxn)

    wids = [i for i, j in enumerate(allrxn) if j == m]

    ws = [options[i] for i in wids]
    if len(ws) > 1:
        winner = '\n\tand\n\t-'.join(ws)
    else:
        winner = ws[0]

    await ctx.channel.send(f'Poll: "{question}" finished. \n\t -{winner} won!')


@client.command()
async def wordsearch(ctx, size, num_words):
    """
    Replies with a randomly generated wordsearch and list of words
    `!wordsearch 10 15` creates a wordsearch 10x10 with 15 words inside.
    """

    try:
        size = int(size)
        num_words = int(num_words)

    except TypeError:
        msg = 'size and num_words parameters must be numbers'
        await ctx.channel.send(msg)

    if size > 25:
        msg = "Unfortunately that's too big for me to send as a message."
        await ctx.channel.send(msg)

    else:

        try:
            ws = Grid(size, num_words, words)
            ws.populate()
            body = ws.prettyprint()
            wordlist = ws.listw()

            await ctx.channel.send(f"```\n{body}\n```")
            await ctx.channel.send(wordlist)

        except StopIteration as e:
            await ctx.channel.send(e)


# fortune cookie commands

# this one generates a fortune based on low training time- 
#   ie bad fortunes that don't make grammatical sense
@client.command(name='fortune', alias=['🥠', 'cookie', ':fortunecookie:'])
async def fortune(ctx):
    """
    Generates a (poorly rendered) imitation of a fortune cookie fortune
    `!fortune` or `!🥠` or `!cookie` all call this command
    """
    
    frtn = bad_fortune_gen()

    await ctx.channel.send(f'*crack*\n\t"{frtn}"\nhmm...')


# this one generates a fortune based on higher training time- 
#   these fortunes tend to be pretty good/make sense
@client.command(name='goodfortune', alias=['good🥠', 'goodcookie', 'good:fortunecookie:'])
async def fortune(ctx):
    """
    Generates a (poorly rendered) imitation of a fortune cookie fortune
    `!goodfortune` or `goodcookie` or `!good🥠` call this command
    """
    
    frtn = good_fortune_gen()

    await ctx.channel.send(f'*crack*\n\t"{frtn}"\nhmm...')

client.run(token)
