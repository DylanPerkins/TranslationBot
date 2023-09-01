import discord

from typing import Union, TYPE_CHECKING
from discord.ext import commands

if TYPE_CHECKING:
    from utilities.default import CustomContext


def can_handle(ctx: "CustomContext", permission: str) -> bool:
    """Checks if bot has permissions or is in DMs right now"""
    return isinstance(ctx.channel, discord.DMChannel) or getattr(
        ctx.channel.permissions_for(ctx.guild.me), permission
    )
