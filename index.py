import discord

from utilities import config, data

config = config.Config.from_env(".testing.env")
print("Logging in...")

bot = data.DiscordBot(
    config=config, command_prefix=config.discord_prefix,
    prefix=config.discord_prefix, command_attrs=dict(hidden=True),
    allowed_mentions=discord.AllowedMentions(
        everyone=False, roles=False, users=True
    ),
    intents=discord.Intents.all()    
)

try:
    bot.run(config.discord_token)
except Exception as e:
    print(f"Error when logging in: {e}")