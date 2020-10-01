import discord
import requests
import asyncio
import dotenv
import os
import sys
import logging
from datetime import datetime
from importlib import reload as reimport
from discord.ext import commands
from io import BytesIO
from threading import Thread
from flask import Flask
import flask

discord.opus.load_opus("libopus.so.0")
dotenv.load_dotenv()
bot = commands.Bot(
    command_prefix=["s.","sj."], activity=discord.Activity(type=discord.ActivityType.streaming, name="s.help"),
    )


@bot.command()
async def ping(ctx):
    """Get the response time for APIs."""
    message = await ctx.send("Pong!")
    await message.edit(
        content=f"Pong!",
        embed=discord.Embed(type="rich")
        .add_field(name="Discord", value=f"{round(bot.latency * 1000)}ms")
        .add_field(
            name="BenBot",
            value=f"{round(requests.get('https://benbotfn.tk/api/v1/status').elapsed.total_seconds() * 1000)}ms",
        )
        .add_field(
            name="FortniteAPIcom",
            value=f"{round(requests.get('https://fortnite-api.com').elapsed.total_seconds() * 1000)}ms",
        )
        .add_field(
            name="FortniteAPIio",
            value=f"{round(requests.get('https://fortniteapi.io').elapsed.total_seconds() * 1000)}ms",
        )
        .add_field(
            name="FortniteTracker",
            value=f"{round(requests.get('https://api.fortnitetracker.com').elapsed.total_seconds() * 1000)}ms",
        )
        .add_field(
            name="NiteStats",
            value=f"{round(requests.get('https://api.nitestats.com').elapsed.total_seconds() * 1000)}ms",
        ),
    )
    inline = True

@bot.command(pass_context=True)
async def invite(ctx):
    embed = discord.Embed(
        color = discord.Colour.blue(),
        title = 'Heres the invite',
        description='[CLICK HERE](https://discord.com/api/oauth2/authorize?client_id=737882571245092984&permissions=0&scope=bot)',
     timestamp = ctx.message.created_at)
    embed.set_footer(text=f'Enjoy the slurp')
    
    embed.set_image(url='https://cdn.discordapp.com/attachments/727759243360337921/755850184335818882/artworks-000496005195-8yqry4-t500x500.png')
   
    await ctx.send(embed=embed)

    


@bot.event
async def on_command_error(ctx, error: commands.CommandError):
    await ctx.send(f"```\n{error}```")



@bot.event
async def on_message(message: discord.Message):
    if message.channel.id == 718979003968520283:
        await asyncio.sleep(2)
        await message.delete()
    else:
        await bot.process_commands(message)


for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        bot.load_extension(f"cogs.{cog[:-3]}")

app = Flask(__name__) #definition of "app" for flask server

@app.route('/') 
def main():
  return 'Running'   #the route for the pings return 'poop'


@bot.event
async def on_ready():
  print("Slurp Juice is Online :)")
  Thread(target=app.run, args=("0.0.0.0", 8080)).start() #this starts the local server



bot.run(os.getenv("TOKEN"))
