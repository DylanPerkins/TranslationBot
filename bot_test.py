import enum
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import deepl
from dotenv import load_dotenv
import os
from language_check import LanguageCheck
from languages import LanguageChoices

# Load the .env file and get some variables
load_dotenv()
auth_key = os.getenv('deepl_auth_key')
bot_token = os.getenv('discord_token')

# Create a bot instance
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents)

# Create a list of language choices for the slash command

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"An error occurred while syncing: {str(e)}")

@client.tree.command(name="translate", description="Translate a message to one of the listed languages. Note: Default language is English.")
async def translate(ctx: commands.Context, message_id: str, language: str):
    try:
        # Check if the supplied message ID is a number
        if not message_id.isdigit():
            return await ctx.response.send_message("Please enter a valid message ID.", ephemeral=True)

        # Fetch the message from the channel
        message = await ctx.channel.fetch_message(int(message_id))
        content = message.content

        if language is None:
            language = "EN-US"
        else:
            language = language.value

        # Translate the message using the DeepL API
        language_name = LanguageCheck.check_language(language)

        translator = deepl.Translator(auth_key)
        result = translator.translate_text(content, target_lang=language)
        translated_text = result.text

        # Send the translated message
        await ctx.response.send_message(f"### Orginal message:\n{content}\n\n### Translated message to __{language_name}__:\n{translated_text}")

    except discord.errors.NotFound:
        await ctx.response.send_message(f"Sorry, I couldn't find a message with that ID (`{message_id}`) in this channel.", ephemeral=True)
    except Exception as e:
        await ctx.response.send_message(f"Whoops! An error occurred while translating the message:\n{str(e)}", ephemeral=True)

@translate.autocomplete("language")
async def language_autocomplete(ctx: commands.Context, argument: str):
    return [choice for choice in LanguageChoices if choice.value.startswith(argument)]

client.run(bot_token)
