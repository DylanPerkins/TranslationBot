import discord_http
import os

from utilities.config import Config


class CustomClient(discord_http.Client):
    def __init__(self, config: Config, *args, **kwargs):
        # Store the config instance and individual parameters
        self.config = config
        self.token = config.discord_token
        self.application_id = config.discord_application_id
        self.public_key = config.discord_public_key
        self.sync = config.discord_sync.lower() == "true"
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        for file in os.listdir("cogs"):
            if not file.endswith(".py"):
                continue  # Skip non-python files

            await self.load_extension(f"cogs.{file[:-3]}")
