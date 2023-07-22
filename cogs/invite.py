import discord
from discord.ext import commands
from utilities.data import DiscordBot
from utilities.default import CustomContext


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot

    @commands.hybrid_command()
    async def invite(self, ctx: CustomContext):
        """Get the invite link for the bot."""
        invite_link = self.bot.config.discord_invite
        await ctx.send(
            f"""
        Thank you for wanting to invite me to your server!\n\nInvite me here -> [Click to Invite Me]({invite_link})
        """
        )


async def setup(bot):
    await bot.add_cog(Invite(bot))
    print("Loaded cog: invite")
