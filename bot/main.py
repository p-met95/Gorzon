import discord
from discord.ext import commands, tasks
import os
import pokepy as pp
from pokedex import *
# import datetime
# import asyncio

client = commands.Bot(command_prefix="!")
token = os.getenv("DISCORD_BOT_TOKEN")

poke_client = pp.V2Client()

special_cases = {
    "Type: Null": "type-null",
    "Mime Jr.": "mime-jr",
    "Mr. Rime": "mr-rime",
    "Mr. Mime": "mr-mime",
    "Tapu Koko": "tapu-koko",
    "Tapu Lele": "tapu-lele",
    "Tapu Bulu": "tapu-bulu",
    "Tapu Fini": "tapu-fini",
    "Farfetch'd": "Farfetchd",
    "Sirfetch'd": "Sirfetchd",
    "Porygon-Z": "Porygon-z"}


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("EATING HUMAN BABIES"))
    print("I am online")
    print(os.getcwd())
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
async def weak(ctx, *, pokemon):
    """Replies with the weaknesses of the pokemon you ask for. Does not account for ability effects: e.g. sap sipper (attempts to spell check)"""
    sug = suggester(pokemon, 'all_pkmn')
    if sug == True:
        if pokemon in special_cases.keys():
            altn = special_cases[pokemon]
            t1, t2 = g_types(altn, poke_client)
            t_name, table = weak_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
        else:
            t1, t2 = g_types(pokemon, poke_client)
            t_name, table = weak_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
    elif len(sug) == 1:
        pokemon = sug[0]
        if pokemon in special_cases.keys():
            altn = special_cases[pokemon]
            t1, t2 = g_types(altn, poke_client)
            t_name, table = weak_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
        else:
            t1, t2 = g_types(pokemon, poke_client)
            t_name, table = weak_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
    elif len(sug) > 1:
        await ctx.channel.send("Did you mean: " + ", ".join(sug[:-1]) + f", or {sug[-1]}?\nPlease ask again with the Pokemon you want.")
    else:
        await ctx.channel.send("Sorry, I couldn't find that.")


@client.command()
async def res(ctx, *, pokemon):
    """Replies with the resistances of the pokemon you ask for. Does not account for ability effects: e.g. sap sipper (attempts to spell check)"""
    sug = suggester(pokemon, 'all_pkmn')
    if sug == True:
        if pokemon in special_cases.keys():
            altn = special_cases[pokemon]
            t1, t2 = g_types(altn, poke_client)
            t_name, table = res_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
        else:
            t1, t2 = g_types(pokemon, poke_client)
            t_name, table = res_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
    elif len(sug) == 1:
        pokemon = sug[0]
        if pokemon in special_cases.keys():
            altn = special_cases[pokemon]
            t1, t2 = g_types(altn, poke_client)
            t_name, table = res_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
        else:
            t1, t2 = g_types(pokemon, poke_client)
            t_name, table = res_table(t1, t2)
            await ctx.channel.send(f"found weaknesses for **__{pokemon}__**:\n```{t_name}\n{table.dumps()}```")
    elif len(sug) > 1:
        await ctx.channel.send("Did you mean: " + ", ".join(sug[:-1]) + f", or {sug[-1]}?\nPlease ask again with the Pokemon you want.")
    else:
        await ctx.channel.send("Sorry, I couldn't find that.")


@client.command()
async def ability(ctx, *, p_ability):
    """Replies with the ability effect you ask for (attempts to spell check)"""
    sug = suggester(p_ability, 'abilities')
    if sug == True:
        alt = p_ability.lower()
        alt = alt.replace(' ', '-')
        abil = g_ability(alt, poke_client)
        await ctx.channel.send(f'**__{p_ability}__**:\n{abil}')
    elif len(sug) == 1:
        p_ability = sug[0]
        alt = p_ability.lower()
        alt = alt.replace(' ', '-')
        abil = g_ability(alt, poke_client)
        await ctx.channel.send(f'**__{p_ability}__**:\n{abil}')
    elif len(sug) > 1:
        await ctx.channel.send("Did you mean: " + ", ".join(sug[:-1]) + f", or {sug[-1]}?\nPlease ask again with the ability you want")
    else:
        await ctx.channel.send("Sorry, I couldn't find that.")

@client.command()
async def move(ctx, *, p_move):
    """Replies with the move power, accuracy, type, and effect you ask for (attempts to spell check)"""
    sug = suggester(p_move, 'moves')
    if sug == True:
        alt = p_move.replace('-', ' ')
        alt = alt.lower()
        alt = alt.replace(' ', '-')
        mov = g_move(alt, poke_client)
        await ctx.channel.send(f'**__{p_move}__**:\n{mov}')
    elif len(sug) == 1:
        p_move = sug[0]
        alt = p_move.replace('-', ' ')
        alt = alt.lower()
        alt = alt.replace(' ', '-')
        mov = g_move(alt, poke_client)
        await ctx.channel.send(f'**__{p_move}__**:\n{mov}')
    elif len(sug) > 1:
        await ctx.channel.send("Did you mean: " + ", ".join(sug[:-1]) + f", or {sug[-1]}?\nPlease ask again with the ability you want")
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

