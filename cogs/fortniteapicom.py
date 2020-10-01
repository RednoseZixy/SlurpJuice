import requests
import discord
from discord.ext import commands
from io import BytesIO


class FortniteAPIcom(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx, mode: str = "br", language: str = None):
        """
        Get the current news as a GIF.
        """
        if mode not in ["br", "stw", "creative"]:
            await ctx.send("```mode has to be one of br, stw, creative```")
            return

        msg = await ctx.send("Loading GIF...", delete_after=120)
        r = requests.get(
            f"https://fortnite-api.com/v2/news/{mode}", params={"language": language}
        ).json()
        gif = r.get("data", {}).get("image", None)
        if gif is not None:
            await ctx.send(
                file=discord.File(
                    fp=BytesIO(requests.get(gif).content), filename="news.gif"
                )
            )
        else:
            await ctx.send("No news image found.")
        await msg.delete()

    @commands.command()
    async def code(self, ctx, code: str):
        """
        Get info on a Creator Code.
        """
        r = requests.get(
            "https://fortnite-api.com/v2/creatorcode", params={"name": code}
        )
        if r.status_code == 404:
            await ctx.send("Cannot Find Creator Code " + code)
        elif r.status_code == 200:
            await ctx.send(
                embed=discord.Embed(title=code, type="rich")
                .add_field(
                    name="Account",
                    value=f"{r.json().get('data', {}).get('account', {}).get('name', 'Unknown')} ({r.json().get('data', {}).get('account', {}).get('id', 'Unknown')})",
                    inline=False,
                )
                .add_field(
                    name="Status",
                    value=r.json().get("data", {}).get("status", "Unknown"),
                    inline=True,
                )
                .add_field(
                    name="Verified",
                    value=r.json().get("data", {}).get("verified", "Unknown"),
                    inline=True,
                )
            )
        else:
            await ctx.send(f"```json\n{r.text}```")


def setup(client: commands.AutoShardedBot):
    client.add_cog(FortniteAPIcom(client))
