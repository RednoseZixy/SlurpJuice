import discord
import twitchio
from discord.ext import commands
from twitchio.ext import commands as tcommands
from os import getenv
from io import BytesIO

bot = tcommands.Bot(
    irc_token=getenv("IRC_TOKEN"),
    client_id=getenv("OAUTH_ID"),
    nick="",
    prefix="s.",
    initial_channels=[],
)


def convert(ls: list):
    return {ls[i]: ls[i + 1] for i in range(0, len(ls), 2)}


class Twitch(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot


def setup(client: commands.AutoShardedBot):
    client.add_cog(Twitch(client))
