import discord
from discord.ext import commands
import deepl
from discord import app_commands, Interaction
from utilities.language_check import LanguageCheck
from utilities.languages import LanguageChoices
from utilities.data import DiscordBot


class TranslateMessage(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot

        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Translate to English", callback=self.translate_to_english
            )
        )

        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Translate to Spanish", callback=self.translate_to_spanish
            )
        )

        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Translate to Chinese", callback=self.translate_to_chinese
            )
        )

        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Translate to French", callback=self.translate_to_french
            )
        )

        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Translate to Ukrainian", callback=self.translate_to_ukrainian
            )
        )

    @commands.hybrid_command()
    async def translate(
        self, ctx: commands.Context, message_link: str, language: LanguageChoices = None
    ):
        """Translate a message to one of the listed languages. Note: Default language is English."""

        auth_key = self.bot.config.deepl_auth_key

        try:
            # Extract the message ID from the message link
            message_id = message_link.split("/")[-1]

            # Check if the supplied message ID is a number
            if not message_id.isdigit():
                return await ctx.send(
                    "Please enter a valid message link.", ephemeral=True
                )

            # Fetch the message from the channel
            message = await ctx.channel.fetch_message(int(message_id))
            content = message.content

            if language is None:
                language = "EN-US"
            else:
                language = language.value

            # Translate the message using the DeepL API
            language_name = LanguageCheck.check_language(language)

            translated_text = translation_api_call(content, auth_key, language)

            # Send the translated message
            await ctx.send(
                f"### Orginal message:\n{content}\n### Translated message to __{language_name}__:\n{translated_text}",
                delete_after=300,
                silent=True,
            )

        except discord.errors.NotFound:
            await ctx.send(
                f"Sorry, I couldn't find a message with that link (`{message_link}`) in this channel.",
                ephemeral=True,
            )
        except Exception as e:
            await ctx.send(
                f"Whoops! An error occurred while translating the message:\n{str(e)}",
                ephemeral=True,
            )

    # Context Menu

    # Translate to English
    async def translate_to_english(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        content = message.content
        auth_key = self.bot.config.deepl_auth_key
        language_name = "English"

        translated_text = translation_api_call(content, auth_key, "EN-US")

        await interaction.response.send_message(
            f"### Orginal message:\n{content}\n### Translated message to __{language_name}__:\n{translated_text}",
            ephemeral=True,
        )

    # Translate to Spanish
    async def translate_to_spanish(
        self, interaction: Interaction, message: discord.Message
    ):
        content = message.content
        auth_key = self.bot.config.deepl_auth_key
        language_name = "Spanish"

        translated_text = translation_api_call(content, auth_key, "ES")

        await interaction.response.send_message(
            f"### Orginal message:\n{content}\n### Translated message to __{language_name}__:\n{translated_text}",
            ephemeral=True,
        )

    # Translate to Chinese (Simplified)
    async def translate_to_chinese(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        content = message.content
        auth_key = self.bot.config.deepl_auth_key
        language_name = "Chinese (Simplified)"

        translated_text = translation_api_call(content, auth_key, "ZH")

        await interaction.response.send_message(
            f"### Orginal message:\n{content}\n### Translated message to __{language_name}__:\n{translated_text}",
            ephemeral=True,
        )

    # Translate to French
    async def translate_to_french(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        content = message.content
        auth_key = self.bot.config.deepl_auth_key
        language_name = "French"

        translated_text = translation_api_call(content, auth_key, "FR")

        await interaction.response.send_message(
            f"### Orginal message:\n{content}\n### Translated message to __{language_name}__:\n{translated_text}",
            ephemeral=True,
        )

    # Translate to Ukrainian
    async def translate_to_ukrainian(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        content = message.content
        auth_key = self.bot.config.deepl_auth_key
        language_name = "Ukrainian"

        translated_text = translation_api_call(content, auth_key, "UK")

        await interaction.response.send_message(
            f"### Orginal message:\n{content}\n### Translated message to __{language_name}__:\n{translated_text}",
            ephemeral=True,
        )


# Translation Function
def translation_api_call(content, auth_key, target_lang):
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(content, target_lang=target_lang)
    translated_text = result.text
    return translated_text


async def setup(bot):
    await bot.add_cog(TranslateMessage(bot))
    print("Loaded cog: translate_message")
