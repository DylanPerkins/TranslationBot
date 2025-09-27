from discord_http import commands, Context, Embed

from utilities.data import CustomClient
from utilities import default


class Discord(commands.Cog):
    def __init__(self, bot):
        self.bot: CustomClient = bot

    server = commands.SubGroup(name="server")

    @server.command(name="info")
    @commands.guild_only()
    async def server_info(self, ctx: Context):
        """Get information about the server"""
        async def call_after():
            guild = await ctx.guild.fetch()
            embed = Embed()

            if guild.icon:
                embed.set_thumbnail(url=guild.icon)
            if guild.banner:
                embed.set_image(url=guild.banner)

            embed.add_field(name="Name", value=guild.name)
            embed.add_field(name="ID", value=guild.id)
            embed.add_field(
                name="Owner", value=f"<@!{guild.owner_id}> ({guild.owner_id})", inline=False)
            embed.add_field(name="Created", value=default.date(
                guild.created_at, ago=True), inline=False)

            await ctx.followup.send(
                f"ℹ️ information about **{guild.name}**",
                embed=embed
            )

        return ctx.response.defer(thinking=True, call_after=call_after)


async def setup(bot: CustomClient):
    await bot.add_cog(Discord(bot))
    print("Loaded cog: discord")
