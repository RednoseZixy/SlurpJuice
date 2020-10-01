import requests
import discord
import asyncio
from discord.ext import commands
from io import BytesIO
from dateutil import parser


def convert(ls: list):
    return {ls[i]: ls[i + 1] for i in range(0, len(ls), 2)}


class NiteStats(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        """
        Show the current BR shop as an image.
        """
        msg = await ctx.send("Loading Shop...")
        image = BytesIO(requests.get("https://api.nitestats.com/v1/shop/image").content)
        await ctx.send(file=discord.File(fp=image, filename="shop.png"))

    @commands.command()
    async def bearer(self, ctx):
        """
        Fetch the current bearer token.
        """
        r = requests.get("https://api.nitestats.com/v1/epic/bearer")
        data = r.json()
        await ctx.send(
            embed=discord.Embed(
                title=data.get("accessToken", "Unknown"),
                type="rich",
                timestamp=parser.parse(data.get("lastUpdated", 0)),
            )
        )

    @commands.command()
    async def font(self, ctx, color: str, size: float, *, text: str):
        """
        Render text in Fortnite's font.
        """
        r = requests.get(
            "https://api.nitestats.com/v1/fnfontgen",
            params={"text": text, "color": color, "size": str(size)},
        )
        if r.status_code != 200:
            await ctx.send(f"```json\n{r.text}```")
        else:
            image = BytesIO(r.content)
            await ctx.send(file=discord.File(fp=image, filename="font.png"))


def setup(client: commands.AutoShardedBot):
    client.add_cog(NiteStats(client))
