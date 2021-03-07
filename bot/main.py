import discord
from discord.ext import commands, tasks
import os
import pokepy as pp
from pokedex import *
import asyncio
import datetime

client = commands.Bot(command_prefix="!")
token = os.getenv("DISCORD_BOT_TOKEN")

poke_client = pp.V2Client()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("EATING HUMAN BABIES"))
    print("I am online")
    # print('starting reminders')
    # what_ya_reading.start()
    # dnd_remind.start()


##
@client.command()
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)


# reminder commands- REFACTOR soon, class? add create your own reminder?

# @tasks.loop(hours=24*7)
# async def what_ya_reading():
#    wid = 774654613894463509
#    ch = client.get_channel(762730040487313488)
#    await ch.send(f'Filthy <@&{wid}>, what degenerecy have you been reading/watching this week?')

# @what_ya_reading.before_loop
# async def before_reading():
#    for _ in range(60*60*24):  # loop the hole day
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
#    for _ in range(60*60*24):  # loop the hole day
#        if datetime.datetime.now().hour - 5 == 4 + 12 and datetime.datetime.now().weekday() == 2:  # wednesday (2) @ 4pm
#            print('pinging party')
#            return
#        await asyncio.sleep(1) # wait a second before looping again. You can make it more


###

@client.command()
async def weak(ctx, pokemon):
    sug = suggester(pokemon, 'all_pkmn')
    if sug == True:
        t1, t2 = g_types(pokemon, poke_client)
        t_name, table = weak_table(t1, t2)
        await ctx.channel.send(f"```{t_name}\n{table.dumps()}```")
    elif len(sug) == 1:
        pokemon = sug[0]
        t1, t2 = g_types(pokemon, poke_client)
        t_name, table = weak_table(t1, t2)
        await ctx.channel.send(f"```{t_name}\n{table.dumps()}```")
    elif len(sug) > 1:
        await ctx.channel.send("Did you mean: " + ", ".join(sug[:-1]) + f", or {sug[-1]}?")
    else:
        await ctx.channel.send("Sorry, I couldn't find that.")


@client.command()
async def res(ctx, pokemon):
    sug = suggester(pokemon, 'all_pkmn')
    if sug == True:
        t1, t2 = g_types(pokemon, poke_client)
        t_name, table = res(t1, t2)
        await ctx.channel.send(f"```{t_name}\n{table.dumps()}```")
    elif len(sug) == 1:
        pokemon = sug[0]
        t1, t2 = g_types(pokemon, poke_client)
        t_name, table = res(t1, t2)
        await ctx.channel.send(f"```{t_name}\n{table.dumps()}```")
    elif len(sug) > 1:
        await ctx.channel.send("Did you mean: " + ", ".join(sug[:-1]) + f", or {sug[-1]}?")
    else:
        await ctx.channel.send("Sorry, I couldn't find that.")

# poll commands

# @client.command(name="poll")
# async def poll(ctx):
#    await ctx.send(f"What is this Poll called?")
#    polltitle = await client.wait_for('')

# @client.event
# async def on_message(msg):
#    if 'Gorzon' in msg.author.diplay_name and '---POLL---' in msg.content:
#        pollcount(msg)

client.run(token)




