import requests
import discord
from discord.ext import commands
from io import BytesIO


def convert(ls: list):
    return {ls[i]: ls[i + 1] for i in range(0, len(ls), 2)}


class BenBot(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx):
        """
        Fetch the current BenBot API Status.
        """
        r = requests.get("https://benbotfn.tk/api/v1/status")
        if r.status_code == 200:
            data = r.json()
            await ctx.send(
                embed=discord.Embed(title="BenBot Status", type="rich")
                .add_field(
                    name="Version",
                    value=f"`{data.get('currentFortniteVersion', 'Unknown')}`",
                    inline=True,
                )
                .add_field(
                    name="CDN Version",
                    value=f"`{data.get('currentCdnVersion', 'Unknown')}`",
                    inline=True,
                )
                .add_field(
                    name="Pak Count",
                    value=f"`{len(data.get('mountedPaks', []))}/{data.get('totalPakCount', 'Unknown')}`",
                    inline=False,
                )
            )
            mounted_paks = ""
            for pak in data.get("mountedPaks", ["Unknown"]):
                mounted_paks = f"{mounted_paks}{pak.split('/')[-1]}\n"
            await ctx.send(
                embed=discord.Embed(
                    title="Mounted Paks", type="rich", description=f"{mounted_paks}"
                )
            )
            all_paks = ""
            for pak in data.get("allPakFiles", ["Unknown"]):
                all_paks = f"{all_paks}{pak.split('/')[-1]}\n"
            await ctx.send(
                embed=discord.Embed(
                    title="All Paks", type="rich", description=f"{all_paks}"
                )
            )

    @commands.command()
    async def aes(self, ctx):
        """
        Fetch the current AES Keys.
        """
        data = requests.get("https://benbotfn.tk/api/v1/aes").json()
        embed = discord.Embed(
            title=data.get("version", "Unknown Version"), type="rich"
        ).add_field(name="**Main Key**", value=data.get("mainKey", "Unknown"))
        for pak in data.get("dynamicKeys", {}):
            embed.add_field(
                name=pak.split("/")[-1],
                value=data.get("dynamicKeys", {}).get(pak, "Unknown"),
                inline=False,
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def id(self, ctx, id: str):
        """
        Show cosmetic info from a cosmetic ID.
        """
        r = requests.get(f"https://benbotfn.tk/api/v1/cosmetics/br/{id}")
        if r.status_code != 200:
            await ctx.send(f"```json\n{r.text}```")
            return
        cosmetic = r.json()
        embed = discord.Embed(
            title=cosmetic.get("name", id),
            type="rich",
            description=f"{cosmetic.get('description', '')}\n{cosmetic.get('setText', 'Not part of any set.')}",
        ).add_field(name="Rarity", value=cosmetic.get("rarity", "Unknown"), inline=True)
        if type(cosmetic.get("series", "")) == dict:
            embed.add_field(
                name="Series", value=cosmetic["series"].get("name", "None"), inline=True
            )
        else:
            embed.add_field(name="Series", value="None", inline=True)
        embed.add_field(
            name="Backend Type",
            value=cosmetic.get("backendType", "Unknown"),
            inline=True,
        ).add_field(
            name="Gameplay Tags",
            value="```" + "\n".join(cosmetic.get("gameplayTags", "None")) + "```",
            inline=False,
        ).add_field(
            name="Path", value="`" + cosmetic.get("path", "Unknown") + "`", inline=False
        )
        if type(cosmetic.get("icons", "")) == dict:
            if cosmetic["icons"].get("icon", None) is not None:
                embed.set_thumbnail(url=cosmetic["icons"]["icon"])
            if cosmetic["icons"].get("featured", None) is not None:
                embed.set_image(url=cosmetic["icons"]["featured"])
        await ctx.send(embed=embed)

    @commands.command()
    async def search(self, ctx, *params):
        """
        Search for a cosmetic.
        """
        r = requests.get(
            "https://benbotfn.tk/api/v1/cosmetics/br/search", params=convert(params)
        )
        if r.status_code != 200:
            await ctx.send(f"""```json\n{r.text}```""")
            return
        cosmetic = r.json()
        embed = discord.Embed(
            title=cosmetic.get("name", cosmetic.get("id", "Unknown")),
            type="rich",
            description=f"{cosmetic.get('description', '')}\n{cosmetic.get('setText', 'Not part of any set.')}",
        ).add_field(name="Rarity", value=cosmetic.get("rarity", "Unknown"), inline=True)
        if type(cosmetic.get("series", "")) == dict:
            embed.add_field(
                name="Series", value=cosmetic["series"].get("name", "None"), inline=True
            )
        else:
            embed.add_field(name="Series", value="None", inline=True)
        embed.add_field(
            name="Backend Type",
            value=cosmetic.get("backendType", "Unknown"),
            inline=True,
        ).add_field(
            name="Gameplay Tags",
            value="```" + "\n".join(cosmetic.get("gameplayTags", "None")) + "```",
            inline=False,
        ).add_field(
            name="Path", value="`" + cosmetic.get("path", "Unknown") + "`", inline=False
        )
        if type(cosmetic.get("icons", "")) == dict:
            if cosmetic["icons"].get("icon", None) is not None:
                embed.set_thumbnail(url=cosmetic["icons"]["icon"])
            if cosmetic["icons"].get("featured", None) is not None:
                embed.set_image(url=cosmetic["icons"]["featured"])
        await ctx.send(embed=embed)

    @commands.command()
    async def extract(self, ctx, path: str, *params):
        """
        Extract an asset from Fortnite's files.
        """
        r = requests.get(
            "https://benbotfn.tk/api/v1/exportAsset",
            params=convert(["path", path] + list(params)),
        )
        if r.status_code != 200:
            await ctx.send(f"""```json\n{r.text}```""")
            return
        elif r.headers.get("Content-Type", None) == "audio/ogg":
            await ctx.send(
                file=discord.File(
                    fp=BytesIO(r.content),
                    filename=r.headers.get("filename", "audio.ogg"),
                )
            )
        elif r.headers.get("Content-Type", None) == "image/png":
            await ctx.send(
                file=discord.File(
                    fp=BytesIO(r.content),
                    filename=r.headers.get("filename", "image.png"),
                )
            )
        elif r.headers.get("Content-Type", None) == "application/json":
            await ctx.send(f"```json\n{r.text}```")
        else:
            await ctx.send(
                f"```Unknown Content-Type: {r.headers.get('Content-Type', 'Unknown')}```"
            )


def setup(client: commands.AutoShardedBot):
    client.add_cog(BenBot(client))
