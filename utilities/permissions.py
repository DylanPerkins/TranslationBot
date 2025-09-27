import discord_http

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord_http import Context


def can_handle(ctx: "Context", permission: str) -> bool:
    """Checks if bot has permissions or is in DMs right now"""
    return isinstance(ctx.channel, discord_http.DMChannel) or getattr(
        ctx.channel.permissions_for(ctx.guild.me), permission
    )
