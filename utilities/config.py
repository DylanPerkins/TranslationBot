from dataclasses import dataclass
from dotenv import dotenv_values

@dataclass
class Config:
    """
    This class is used to store the bot's configuration.
    """
    discord_token: str
    discord_application_id: str
    discord_public_key: str
    discord_prefix: str
    discord_owner_guild_id: str
    discord_error_webhook: str
    discord_invite: str

    deepl_auth_key: str

    @classmethod
    def from_dict(cls, **kwargs) -> "Config":
        """ Create a Config object from a dictionary. """
        kwargs_overwrite = {}

        for k, v in kwargs.items():
            new_key = k.lower()

            if v.isdigit():
                kwargs_overwrite[new_key] = int(v)
            else:
                kwargs_overwrite[new_key] = v

        return Config(**kwargs_overwrite)

    @classmethod
    def from_env(cls, filename: str = ".env") -> "Config":
        """ Create a Config object from a .env file. """
        return Config.from_dict(**dotenv_values(filename))