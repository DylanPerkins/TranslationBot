import time
import json
import discord
import traceback

from discord.ext import commands
from typing import TYPE_CHECKING
from datetime import datetime
from io import BytesIO

if TYPE_CHECKING:
    from utilities.data import DiscordBot


class CustomContext(commands.Context):
    """
    This class is used to overwrite discord.py's Context class.
    You can add your own methods here.
    Any functions you add will automatically become usable in ALL commands.

    Example:
    --------
    def ping(self) -> str:
        return "Hello world!"

    @commands.command()
    async def ping(self, ctx: CustomContext):
        await ctx.send(f"Pong! {ctx.ping()}")
    """

    def __init__(self, **kwargs):
        self.bot: "DiscordBot"
        super().__init__(**kwargs)


async def send_message(self, content, **kwargs):
    await self.send(content, **kwargs)


def traceback_maker(err, advance: bool = True) -> str:
    """A way to debug your code anywhere"""
    _traceback = "".join(traceback.format_tb(err.__traceback__))
    error = f"```py\n{_traceback}{type(err).__name__}: {err}\n```"
    return error if advance else f"{type(err).__name__}: {err}"


def timetext(name) -> str:
    """Timestamp, but in text form"""
    return f"{name}_{int(time.time())}.txt"


def date(target, clock: bool = True, ago: bool = False, only_ago: bool = False) -> str:
    """Converts a timestamp to a Discord timestamp format"""
    if isinstance(target, int) or isinstance(target, float):
        target = datetime.utcfromtimestamp(target)

    unix = int(time.mktime(target.timetuple()))
    timestamp = f"<t:{unix}:{'f' if clock else 'D'}>"
    if ago:
        timestamp += f" (<t:{unix}:R>)"
    if only_ago:
        timestamp = f"<t:{unix}:R>"
    return timestamp


async def pretty_results(
    ctx: CustomContext,
    filename: str = "Results",
    resultmsg: str = "Here's the results:",
    loop: list = None,
) -> None:
    """A prettier way to show loop results"""
    if not loop:
        return await ctx.send("The result was empty...")

    pretty = "\r\n".join(
        [f"[{str(num).zfill(2)}] {data}" for num, data in enumerate(loop, start=1)]
    )

    if len(loop) < 15:
        return await ctx.send(f"{resultmsg}```ini\n{pretty}```")

    data = BytesIO(pretty.encode("utf-8"))
    await ctx.send(
        content=resultmsg, file=discord.File(data, filename=timetext(filename.title()))
    )
