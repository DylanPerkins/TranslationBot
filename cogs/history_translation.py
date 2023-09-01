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

            # Check if the supplied message ID is a number
            if not isinstance(message_id_top, int) or message_id_top <= 0:
                return await ctx.send(
                    "Please enter a valid starting message link.", ephemeral=True
                )
            if not isinstance(message_id_bottom, int) or message_id_bottom <= 0:
                return await ctx.send(
                    "Please enter a valid ending message link.", ephemeral=True
                )

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

            # Find the message data between the message links
            if not message_objects or message_objects[0].id != message_id_top:
                # Fetch the 'top' message link data
                try:
                    top_message = await ctx.channel.fetch_message(message_id_top)
                    message_objects.insert(0, top_message)
                except discord.NotFound:
                    pass

            if not message_objects or message_objects[-1].id != message_id_bottom:
                # Fetch the 'bottom' message link data
                try:
                    bottom_message = await ctx.channel.fetch_message(message_id_bottom)
                    message_objects.append(bottom_message)
                except discord.NotFound:
                    pass

            message_content = "\n".join(message.content for message in message_objects)

            if not message_content:
                return await ctx.send(
                    "No message content found between the specified message links. Maybe try different links?",
                    ephemeral=True,
                )

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
            await ctx.send(links_message)

            # Fetch the message id of the links_message
            links_message_id = fetch_message_id(self, links_message)

            # Create a public thread on the original message
            thread = await create_thread(ctx, int(links_message_id))

            # Send the original and translated content in the new public thread
            await thread.send(
                f"### Original Message Content:\n{message_content}"
            )
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

async def create_thread(ctx: commands.Context, message_id: int):
    thread_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    thread = await discord.message.Message.create_thread(
        self=ctx.message.channel.fetch_message(message_id),
        name=f"Translation Thread by {ctx.author} - {thread_name}",
        reason="Thread for message translation",
    )
    return thread

# Fetch the message id of the links_message
async def fetch_message_id(self, message):
    return message.id


async def setup(bot):
    await bot.add_cog(TranslateMessageHistory(bot))
    print("Loaded cog: history_translation")
