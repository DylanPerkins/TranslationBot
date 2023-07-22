import discord
from discord.ext import commands
from utilities.data import DiscordBot
from utilities.default import CustomContext


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot

    @commands.hybrid_command()
    async def sync(self, ctx: CustomContext, user: discord.User = None):
        """Sync the commands with discord."""

        if user is None:
            user = ctx.author

        if self.bot.config.discord_owner_id == user.id:
            await self.bot.tree.sync()
            await ctx.send("Synced commands with discord.")
        else:
            await ctx.send("You are not the owner of this bot :P Nice try though!.")


async def setup(bot):
    await bot.add_cog(Sync(bot))
    print("Loaded cog: sync")
