import discord
import os

from utilities import permissions, default
from utilities.config import Config
from discord.ext.commands import AutoShardedBot


class DiscordBot(AutoShardedBot):
    def __init__(self, config: Config, prefix: list[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix
        self.config = config

    async def setup_hook(self):
        for file in os.listdir("cogs"):
            if not file.endswith(".py"):
                continue  # Skip non-python files

            name = file[:-3]
            await self.load_extension(f"cogs.{name}")

    async def on_message(self, msg: discord.Message):
        if (
            not self.is_ready()
            or msg.author.bot
            or not permissions.can_handle(msg, "send_messages")
        ):
            return

        await self.process_commands(msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=default.CustomContext)
        await self.invoke(ctx)
