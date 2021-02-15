import discord
from discord.ext import commands, tasks
import os
import asyncio
import pytz
import datetime

client = commands.Bot(command_prefix="!")
token = os.getenv("DISCORD_BOT_TOKEN")
curguild = client.get_guild()
print(curguild)

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("READY TO DEVOUR PUNY HUMANS"))
    print("I am online")


@client.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx):
    await ctx.send(f"You are {ctx.message.author.name}")

@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

# actual commands

#@tasks.loop(hours=168)
@tasks.loop(minutes=5)
async def what_ya_reading(curguild):
    #w = 774654613894463509
    w = 702161224036515870
    ch = client.get_channel(809557994684809257)
    weebs = discord.utils.get(curguild.roles, id=w)
    await ch.send(f'Filthy {weebs.mention}, what degenerecy are you reading/watching this week?')

@what_ya_reading.before_loop
async def before_reading(curguild):
    for _ in range(60*60*24):  # loop the hole day
        if pytz.timezone('US/Eastern').localize(datetime.datetime.now()).hour == 19:  # 24 hour format
            print('It is time')
            return
        await asyncio.sleep(1) # wait a second before looping again. You can make it more


#@tasks.loop(hours=168)
#async def dnd_reminder(ctx):
#    party = discord.utils.get(ctx.guild.roles, id=570382098121097226)
#    await ctx.send(f'Feeble {weebs.mention}, the session start is 7:30PM EST')

#@client.command(name="poll")
#async def poll(ctx):
#    await ctx.send(f"---POLL---\n---{time}---\n{pollname}\n\t:emoji1:{option1}\n\t:emoji2:{option2}")

#@client.event
#async def on_message(msg):
#    if 'Gorzon' in msg.author.diplay_name and '---POLL---' in msg.content:
#        pollcount(msg)

client.run(token)