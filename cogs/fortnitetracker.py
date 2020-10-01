import requests
import discord
from discord.ext import commands
from os import getenv


def convert(ls: list):
    return {ls[i]: ls[i + 1] for i in range(0, len(ls), 2)}


class FortniteTracker(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.headers = {"TRN-Api-Key": getenv("TRN_API_KEY")}

    @commands.command()
    async def stats(self, ctx, platform: str, *, name: str):
        """
        Retrieve a user's in-game stats.
        Platforms: kbm, gamepad, touch
        """
        platform = platform.lower()
        if platform not in ["kbm", "gamepad", "touch"]:
            await ctx.send(
                "Invalid Platform! Valid platforms are: `kbm`, `gamepad`, `touch`"
            )
            return
        r = requests.get(
            f"https://api.fortnitetracker.com/v1/profile/{platform}/{name}",
            headers=self.headers,
        )
        if r.status_code == 404:
            await ctx.send("Cannot Find User " + name)
            return
        else:
            data = r.json()
            embed = discord.Embed(
                title=f"{data.get('epicUserHandle', name)} ({data.get('platformNameLong', platform)})",
                type="rich",
            )
            stats = data.get("lifeTimeStats", {})
            for s in stats:
                embed.add_field(
                    name=s.get("key", "Unknown"), value=s.get("value", "Unknown")
                )
            await ctx.send(embed=embed)


def setup(client: commands.AutoShardedBot):
    client.add_cog(FortniteTracker(client))
