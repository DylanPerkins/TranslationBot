import enum
import discord
from discord.ext import commands
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

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"An error occurred while syncing: {str(e)}")


@client.tree.command()
async def translate(ctx: commands.Context, message_id: str, language: LanguageChoices = None):
    """ Translate a message to one of the listed languages. Note: Default language is English. """

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

        translated_text = translation_api_call(content, language)

        # Send the translated message
        await ctx.response.send_message(f"### Orginal message:\n{content}\n### Translated message to __{language_name}__:\n{translated_text}")

    except discord.errors.NotFound:
        await ctx.response.send_message(f"Sorry, I couldn't find a message with that ID (`{message_id}`) in this channel.", ephemeral=True)
    except Exception as e:
        await ctx.response.send_message(f"Whoops! An error occurred while translating the message:\n{str(e)}", ephemeral=True)

# Context menus (right click menus)
# Note: Max of 5

# Translate to English
@client.tree.context_menu(name="Translate to English")
async def translate_to_english(interaction: discord.Interaction, message: discord.Message):
    content = message.content

    translated_text = translation_api_call(content, "EN-US")

    await interaction.response.send_message(f"Translated message to __English__:\n{translated_text}", ephemeral=True)


# Translate to Spanish
@client.tree.context_menu(name="Translate to Spanish")
async def translate_to_english(interaction: discord.Interaction, message: discord.Message):
    content = message.content

    translated_text = translation_api_call(content, "ES")

    await interaction.response.send_message(f"Translated message to __Spanish__:\n{translated_text}", ephemeral=True)


# Translate to Chinese (Simplified)
@client.tree.context_menu(name="Translate to Chinese")
async def translate_to_english(interaction: discord.Interaction, message: discord.Message):
    content = message.content

    translated_text = translation_api_call(content, "ZH")

    await interaction.response.send_message(f"Translated message to __Chinese (Simplified)__:\n{translated_text}", ephemeral=True)


# Translate to French
@client.tree.context_menu(name="Translate to French")
async def translate_to_english(interaction: discord.Interaction, message: discord.Message):
    content = message.content

    translated_text = translation_api_call(content, "FR")

    await interaction.response.send_message(f"Translated message to __French__:\n{translated_text}", ephemeral=True)


# Translate to Ukrainian
@client.tree.context_menu(name="Translate to Ukrainian")
async def translate_to_english(interaction: discord.Interaction, message: discord.Message):
    content = message.content

    translated_text = translation_api_call(content, "UK")

    await interaction.response.send_message(f"Translated message to __Ukrainian__:\n{translated_text}", ephemeral=True)

# Translation Function
def translation_api_call(content, target_lang):
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(content, target_lang=target_lang)
    translated_text = result.text
    return translated_text


client.run(f"{bot_token}")
