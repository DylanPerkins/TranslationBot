import deepl

from discord_http import Context, commands, Message, Member
import discord_http.errors as error

from utilities.language_check import LanguageCheck
from utilities.data import CustomClient
from utilities.config import Config

config = Config.from_env(".env")

# Error message
message_too_long = "Sorry, I couldn't send the translated message because the message was too long!"


class TranslateMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: CustomClient = bot

    server = commands.SubGroup(name="translate")

    @server.command(name="message")
    async def translate(
        self, ctx: Context, message_link: str, language: str = None
    ):
        """Translate a message to one of the listed languages. Note: Default language is English."""

        async def call_after():
            auth_key = config.deepl_auth_key

            # Set default target language to English if none is provided
            target_language = language if language is not None else "EN-US"

            try:
                # Extract the message ID from the message link
                message_id = message_link.split("/")[-1]

                # Check if the supplied message ID is a number
                if not message_id.isdigit():
                    await ctx.edit_original_response(
                        content="Please enter a valid message link."
                    )
                    return

                # Fetch the message from the channel
                try:
                    message = await ctx.channel.fetch_message(int(message_id))
                except error.NotFound:
                    await ctx.edit_original_response(
                        content=f"Sorry, I couldn't find a message with that link (`{message_link}`) in this channel."
                    )
                    return

                content = message.content

                # Translate the message using the DeepL API
                target_language_name = LanguageCheck.check_language(
                    target_language)

                translated_text, source_language = translation_api_call(
                    content, auth_key, target_language
                )

                source_language_name = LanguageCheck.check_language(
                    source_language)

                # Send the translated message
                try:
                    await ctx.edit_original_response(
                        content=f"**Original language:** *{source_language_name}*\n### Translated message to __{target_language_name}__:\n{translated_text}"
                    )
                except error.DiscordException:
                    await ctx.edit_original_response(
                        content=message_too_long
                    )
            except Exception as e:
                await ctx.edit_original_response(
                    content=f"Whoops! An error occurred while translating the message:\n{str(e)}"
                )

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)

    # Translate Conversation History Command
    @server.command(name="history")
    async def translate_history(
        self,
        ctx: Context,
        bottom_message_link: str,
        top_message_link: str,
        member: Member = None,
        language: str = None
    ):
        """Translate your conversation history to one of the listed languages."""

        async def call_after():
            auth_key = config.deepl_auth_key

            # Set default target language to English if none is provided
            target_language = language if language is not None else "EN-US"

            member = ctx.user

            try:
                # Extract the message IDs from the message links
                try:
                    message_id_top = top_message_link.split("/")[-1]
                    message_id_bottom = bottom_message_link.split("/")[-1]

                    # Validate message IDs are numbers
                    if not message_id_top.isdigit() or not message_id_bottom.isdigit():
                        await ctx.edit_original_response(
                            content="Please enter valid message links."
                        )
                        return

                    message_id_top = int(message_id_top)
                    message_id_bottom = int(message_id_bottom)

                except (ValueError, IndexError):
                    await ctx.edit_original_response(
                        content="Please enter valid message links."
                    )
                    return

                # Fetch the messages from the channel
                try:
                    top_message = await ctx.channel.fetch_message(message_id_top)
                    bottom_message = await ctx.channel.fetch_message(message_id_bottom)
                except error.NotFound:
                    await ctx.edit_original_response(
                        content="Sorry, I couldn't find one of the messages with those links in this channel."
                    )
                    return

                # Get the message objects from the message IDs
                message_objects = []
                limit = 100  # Message limit

                # Fetch the messages between the top and bottom messages
                async for message in ctx.channel.fetch_history(
                    before=bottom_message.id,
                    after=top_message.id,
                    limit=limit
                ):
                    if message.content:  # Only add messages with content
                        message_objects.append(message.content)

                # Add the boundary messages
                message_objects.insert(0, top_message.content)
                message_objects.append(bottom_message.content)

                # Filter out empty messages and join content
                message_content = "\n".join(
                    [msg for msg in message_objects if msg.strip()])

                if not message_content.strip():
                    await ctx.edit_original_response(
                        content="No message content found to translate."
                    )
                    return

                # Translate the message using the DeepL API
                target_language_name = LanguageCheck.check_language(
                    target_language)

                translated_text, source_language = translation_api_call(
                    message_content, auth_key, target_language
                )

                source_language_name = LanguageCheck.check_language(
                    source_language)

                # Send the message links in the same channel
                links_message = (
                    f"**Top Message Link:** {top_message_link}\n"
                    f"**Bottom Message Link:** {bottom_message_link}"
                )

                try:
                    links_message_object = await ctx.channel.send(links_message)

                    thread = await links_message_object.create_public_thread(
                        name=f"Translation Thread by {member.display_name}",
                        reason="Thread for message translation",
                    )

                    # Send the original and translated content in the new public thread
                    await thread.send(f"### Original Message Content:\n{message_content}")
                    await thread.send(
                        f"**Original language:** *{source_language_name}*\n### Translated Message Content to __{target_language_name}__:\n{translated_text}"
                    )

                    await ctx.edit_original_response(
                        content="Successfully translated the conversation history! Check the thread created in this channel."
                    )

                except error.DiscordException:
                    await ctx.edit_original_response(
                        content=message_too_long
                    )

            except Exception as e:
                await ctx.edit_original_response(
                    content=f"Whoops! An error occurred while translating the messages:\n{str(e)}"
                )

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)

    @translate.autocomplete("language")
    async def translate_autocomplete(self, ctx: Context, current: str):
        # Filter the languages based on the current input
        filtered_languages = {
            key: value
            for key, value in LanguageCheck.LANGUAGES.items()
            if current.lower() in key.lower() or current.lower() in value.lower()
        }

        return ctx.response.send_autocomplete(filtered_languages)

    # Context Menu Commands

    async def translate_tree_func(self, ctx: Context, message: Message, language_code: str, target_language_name: str):
        """Common function for all message command translations"""
        content = message.content
        auth_key = config.deepl_auth_key

        try:
            translated_text, source_language = translation_api_call(
                content, auth_key, language_code
            )

            source_language_name = LanguageCheck.check_language(
                source_language)

            await ctx.edit_original_response(
                content=f"**Original language:** *{source_language_name}*\n### Translated message to __{target_language_name}__:\n{translated_text}"
            )
        except error.DiscordException:
            await ctx.edit_original_response(
                content=message_too_long
            )

    @commands.message_command(name="Translate to English")
    async def translate_to_english(self, ctx: Context, message: Message):
        async def call_after():
            await self.translate_tree_func(ctx, message, "EN-US", "English")

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)

    @commands.message_command(name="Translate to Spanish")
    async def translate_to_spanish(self, ctx: Context, message: Message):
        async def call_after():
            await self.translate_tree_func(ctx, message, "ES", "Spanish")

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)

    @commands.message_command(name="Translate to Chinese")
    async def translate_to_chinese(self, ctx: Context, message: Message):
        async def call_after():
            await self.translate_tree_func(ctx, message, "ZH", "Chinese (Simplified)")

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)

    @commands.message_command(name="Translate to French")
    async def translate_to_french(self, ctx: Context, message: Message):
        async def call_after():
            await self.translate_tree_func(ctx, message, "FR", "French")

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)

    @commands.message_command(name="Translate to Ukrainian")
    async def translate_to_ukrainian(self, ctx: Context, message: Message):
        async def call_after():
            await self.translate_tree_func(ctx, message, "UK", "Ukrainian")

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)


# Translation Function
def translation_api_call(content, auth_key, target_lang):
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(content, target_lang=target_lang)
    translated_text = result.text
    source_language = result.detected_source_lang
    return translated_text, source_language


async def setup(bot: CustomClient):
    await bot.add_cog(TranslateMessage(bot))
    print("Loaded cog: translate_message")
