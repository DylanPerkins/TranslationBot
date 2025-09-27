from discord_http import commands, Context, Embed

from utilities.data import CustomClient
from utilities import default


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot: CustomClient = bot

    server = commands.SubGroup(name="bot")

    @server.command(name="info")
    @commands.guild_only()
    async def bot_info(self, ctx: Context):
        """Get information about the bot"""
        async def call_after():
            embed = Embed()

            embed.add_field(name="Name", value=self.bot.user.name)
            embed.add_field(name="ID", value=self.bot.user.id)
            embed.add_field(name="Created", value=default.date(
                self.bot.user.created_at, ago=True), inline=False)

            await ctx.edit_original_response(
                content=f"ℹ️ information about **{self.bot.user.name}**",
                embed=embed
            )

        return ctx.response.defer(thinking=True, call_after=call_after)

    @server.command(name="invite")
    @commands.guild_only()
    async def invite(self, ctx: Context):
        """Get the bot invite link"""
        invite_link = self.bot.config.discord_invite
        await ctx.send(
            f"""
        Thank you for wanting to invite me to your server!\n\nInvite me here -> [Click to Invite Me]({invite_link})
        """
        )


async def setup(bot: CustomClient):
    await bot.add_cog(Bot(bot))
    print("Loaded cog: bot")
