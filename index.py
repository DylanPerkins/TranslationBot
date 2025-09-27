from discord_http.gateway import Intents

from utilities import config
from utilities.data import CustomClient

config = config.Config.from_env(".env")
print("Logging in...")

client = CustomClient(
    config=config,
    token=config.discord_token,
    application_id=config.discord_application_id,
    public_key=config.discord_public_key,
    sync=config.discord_sync.lower() == "true",
    intents=Intents(1)
)

# Run bot
try:
    client.start()
except Exception as e:
    print(f"Error when logging in: {e}")
