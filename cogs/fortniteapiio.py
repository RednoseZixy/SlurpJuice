import requests
import discord
import json
from os import getenv
from discord.ext import commands
from io import BytesIO
from dateutil import parser
from time import time


def convert(ls: list):
    return {ls[i]: ls[i + 1] for i in range(0, len(ls), 2)}


class FortniteAPIio(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.headers = {"Authorization": getenv("IO_API_KEY")}

    @commands.command()
    async def map(self, ctx):
        """
        Get the current Battle Royale map.
        """
        msg = await ctx.send("Loading Map...")
        image = BytesIO(
            requests.get(
                "https://media.fortniteapi.io/images/map.png", headers=self.headers
            ).content
        )
        await ctx.send(file=discord.File(fp=image, filename="map.png"))
        await msg.delete()

    @commands.command()
    async def featured_islands(self, ctx):
        """
        Show the current Creative Featured Islands.
        WARNING: This command can potentially spam chat!
        """
        r = requests.get(
            "https://fortniteapi.io/creative/featured", headers=self.headers
        )
        data = r.json()
        for island in data.get("featured", {}):
            embed = (
                discord.Embed(
                    title=island.get("title", "Unknown"),
                    type="rich",
                    timestamp=parser.parse(island.get("publishedDate", None)),
                    description=island.get("introduction", None),
                )
                .set_author(name=island.get("code", "0000-0000-0000"))
                .set_image(url=island.get("image", None))
                .set_thumbnail(url=island.get("islandPlotTemplate", {}).get("image"))
            )
            tags = ""
            for tag in island.get("tags", []):
                tags = f"{tags}{tag} "
            embed.set_footer(text=tags)
            await ctx.send(embed=embed)

    @commands.command()
    async def island(self, ctx, island_code: str):
        """
        Get info on a Creative island.
        """
        if len(island_code.split("-")) != 3 or len(island_code) != 14:
            await ctx.send(
                "Invalid Island Code Format! Please format your code like this: `0000-0000-0000`"
            )
            return
        r = requests.get(
            "https://fortniteapi.io/creative/island",
            headers=self.headers,
            params={"code": island_code},
        )
        if not r.json().get("response", True):
            await ctx.send(f"```{r.json().get('message', 'unknown error')}```")
            return
        island = r.json().get("island", {})
        embed = (
            discord.Embed(
                title=island.get("title", "Unknown"),
                type="rich",
                timestamp=parser.parse(island.get("publishedDate", None)),
                description=island.get("introduction", None),
            )
            .set_author(name=island.get("code", "0000-0000-0000"))
            .set_image(url=island.get("image", None))
            .set_thumbnail(url=island.get("islandPlotTemplate", {}).get("image"))
        )
        tags = ""
        for tag in island.get("tags", []):
            tags = f"{tags}{tag} "
        embed.set_footer(text=tags)
        await ctx.send(embed=embed)

    @commands.command()
    async def challenges(
        self, ctx, type: str = None, arg: str = None, lang: str = "en"
    ):
        """
        Show the current and upcoming BR challenges.
        Types: weekly, limited_time
        For weekly, arg is the week number.
        WARNING: This command can potentially spam chat!
        """
        if type not in ["weekly", "limited_time", None]:
            await ctx.send(
                "```type must be one of 'weekly', 'limited_time', or None```"
            )
            return
        elif arg.lower() == "none":
            arg = None
        r = requests.get(
            "https://fortniteapi.io/challenges",
            headers=self.headers,
            params={"season": "current", "lang": lang},
        )
        if r.status_code != 200:
            await ctx.send(f"```json\n{r.text}```")
        elif type == "weekly":
            if arg is None:
                for week in r.json().get("weeks", {}):
                    week = r.json().get("weeks", {}).get(week, {})
                    embed = discord.Embed(
                        title=week.get("name", "Unknown"),
                        type="rich",
                        color=int(f"0x{week.get('color', '000000')}", 16),
                    )
                    for challenge in week.get("challenges", {}):
                        embed.add_field(
                            name=challenge.get("title", "Unknown"),
                            value=f"/{challenge.get('progress_total', '0')} • {challenge.get('xp', '0')} XP • {challenge.get('quest_id', '')}",
                            inline=False,
                        )
                    await ctx.send(embed=embed)
            else:
                week = r.json().get("weeks", {}).get(arg, None)
                if week is None:
                    await ctx.send(f"```Cannot Find Week {arg}```")
                else:
                    embed = discord.Embed(
                        title=week.get("name", "Unknown"),
                        type="rich",
                        color=int(f"0x{week.get('color', '000000')}", 16),
                    )
                    for challenge in week.get("challenges", {}):
                        embed.add_field(
                            name=challenge.get("title", "Unknown"),
                            value=f"Required: {challenge.get('progress_total', '0')} • {challenge.get('xp', '0')} XP • {challenge.get('quest_id', '')}",
                            inline=False,
                        )
                    await ctx.send(embed=embed)
        elif type == "limited_time":
            packs = r.json().get("limited_time", {}).get("current", {})
            if packs is None:
                await ctx.send("There are no current limited time challenges to show.")
                return
            else:
                await ctx.send("This command is still in development.")


def setup(client: commands.AutoShardedBot):
    client.add_cog(FortniteAPIio(client))
