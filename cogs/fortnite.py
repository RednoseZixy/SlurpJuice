import fortnitepy
import discord
import asyncio
from os import getenv
from discord.ext import commands


class FnPyClient(fortnitepy.Client):
    def __init__(self):
        super().__init__(
            auth=fortnitepy.AdvancedAuth(
                device_id=getenv("DEVICE_ID"),
                account_id=getenv("ACCOUNT_ID"),
                secret=getenv("SECRET"),
            )
        )

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.start())

    async def event_ready(self):
        for f in list(self.pending_friends.values()):
            await f.reject()
        for f in list(self.friends.values()):
            if f.id != "1461dd380edd4519ab4041ab63e05832":
                await f.remove()


class FortnitePy(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.client = FnPyClient()


def setup(client: commands.AutoShardedBot):
    pass
