import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import deepl
from dotenv import load_dotenv
import os

load_dotenv()

auth_key = os.getenv('deepl_auth_key')
bot_token = os.getenv('discord_token')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"An error occurred while syncing: {str(e)}")


# TODO: Gets error `AttributeError: 'Interaction' object has no attribute 'send' ` 
@bot.tree.command()
async def translate(ctx: commands.Context, message_id: str):
    try:
        # Fetch the message from the channel
        
        if not message_id.isdigit():
            return await ctx.send("Please enter a valid message ID.")

        message = await ctx.fetch_message(int(message_id))
        content = message.content

        translator = deepl.Translator(auth_key)

        result = translator.translate_text(content, target_lang="FR")
        translated_text = result.text

        await ctx.send(f"Translated message: {translated_text}")
    except discord.errors.NotFound:
        await ctx.send(f"Sorry, I couldn't find a message with the ID of  {message_id} in this channel.")
    except Exception as e:
        await ctx.send(f"An error occurred while translating the message: {str(e)}")

@bot.tree.context_menu(name="Translate to English")
async def translate_to_english(interaction: discord.Interaction, message: discord.Message):
    content = message.content

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(content, target_lang="EN-US")
    translated_text = result.text

    await interaction.response.send_message(f"Translated message: {translated_text}", ephemeral=True)

bot.run(f"{bot_token}")