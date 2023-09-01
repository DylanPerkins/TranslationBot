import discord
from discord.ext import commands
from cogs.translate_message import translation_api_call
from utilities.language_check import LanguageCheck
from utilities.languages import LanguageChoices
from utilities.data import DiscordBot
import datetime


# Create a Class named TranslateMessageHistory, inheriting from commands.Cog
class TranslateMessageHistory(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot

    @commands.hybrid_command()
    async def translate_history(
        self,
        ctx: commands.Context,
        bottom_message_link: str,
        top_message_link: str,
        language: LanguageChoices = None,
    ):
        """Translate your conversation history to one of the listed languages."""

        auth_key = self.bot.config.deepl_auth_key

        try:
            # Extract the message ID from the message links
            message_id_top = int(top_message_link.split("/")[-1])
            message_id_bottom = int(bottom_message_link.split("/")[-1])

            try:
                top_message = await ctx.channel.fetch_message(message_id_top)
            except discord.NotFound:
                return await ctx.send("Message not found. Please try again.")

            try:
                bottom_message = await ctx.channel.fetch_message(message_id_bottom)
            except discord.NotFound:
                return await ctx.send("Message not found. Please try again.")

            # Get the message objects from the message IDs
            message_objects = []
            limit = 100  # Message limit

            async for message in ctx.channel.history(
                limit=limit,
                after=discord.Object(id=message_id_top),
                before=discord.Object(id=message_id_bottom),
                oldest_first=True,
            ):
                message_objects.append(message)

            message_objects.insert(0, top_message)
            message_objects.append(bottom_message)

            message_content = "\n".join(message.content for message in message_objects)

            # DeepL API Call
            if language is None:
                language = "EN-US"
            else:
                language = language.value

            # Set the language name based on its language code
            language_name = LanguageCheck.check_language(language)

            translated_message = translation_api_call(
                message_content, auth_key, language
            )

            # Send the message links in the same channel
            links_message = (
                f"**Top Message Link:** {top_message_link}\n"
                f"**Bottom Message Link:** {bottom_message_link}"
            )
            links_message_object = await ctx.send(links_message)

            thread = await links_message_object.create_thread(
                name=f"Translation Thread by {ctx.author}",
                reason="Thread for message translation",
            )

            # Send the original and translated content in the new public thread
            await thread.send(f"### Original Message Content:\n{message_content}")
            await thread.send(
                f"### Translated Message Content to __{language_name}__:\n{translated_message}"
            )

        except discord.errors.NotFound:
            await ctx.send(
                f"Sorry, I couldn't find a message with either (`{bottom_message_link}` or `{top_message_link}`) in this channel.",
                ephemeral=True,
            )
        except Exception as e:
            await ctx.send(
                f"Whoops! An error occurred while translating the message:\n{str(e)}",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(TranslateMessageHistory(bot))
    print("Loaded cog: history_translation")
