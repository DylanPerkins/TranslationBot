import discord
from discord.ext import commands
import deepl
from dotenv import load_dotenv
import os

load_dotenv()

auth_key = os.getenv('deepl_auth_key')
bot_token = os.getenv('discord_token')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@commands.hybrid_command()
async def translate(ctx: commands.Context, message_id: int):
    try:
        message = await ctx.channel.fetch_message(message_id)
        content = message.content

        translator = deepl.Translator(auth_key)

        result = translator.translate_text({content}, target_lang="FR")
        translated_text = result.text

        await ctx.send(f"Translated message: {translated_text}")
    except discord.errors.NotFound:
        await ctx.send(f"Sorry, I couldn't find a message with ID {message_id} in this channel.")
    except Exception as e:
        await ctx.send(f"An error occurred while translating the message: {str(e)}")

bot.add_command(translate)
bot.run(f"{bot_token}")