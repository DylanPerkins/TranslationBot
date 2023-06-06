import discord
from discord.ext import commands
import deepl
from dotenv import load_dotenv
import os
from languages import LanguageChoices

load_dotenv()
auth_key = os.getenv('deepl_auth_key')
bot_token = os.getenv('discord_token')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    try:
        await bot.sync_commands()
        print("Synced commands successfully.")
    except Exception as e:
        print(f"An error occurred while syncing commands: {str(e)}")

@bot.slash_command(
    name="translate",
    description="Translate a message to one of the listed languages. Note: Default language is English."
)
async def translate(ctx: commands.SlashContext, message_id: int, language: LanguageChoices = None):
    try:
        message = await ctx.channel.fetch_message(message_id)
        content = message.content

        if language is None:
            language = LanguageChoices.EN_US
        else:
            language = language.value

        language_name = language.name

        translator = deepl.Translator(auth_key)
        result = translator.translate_text(content, target_lang=language)
        translated_text = result.text

        await ctx.send(f"Translated message to __{language_name}__:\n{translated_text}")

    except discord.NotFound:
        await ctx.send(f"Sorry, I couldn't find a message with that ID (`{message_id}`) in this channel.")
    except Exception as e:
        await ctx.send(f"An error occurred while translating the message:\n{str(e)}")

bot.run(bot_token)
