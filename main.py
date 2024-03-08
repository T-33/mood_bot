#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import random
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def lebron_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    directory = "photos/"
    random_image = random.choice(os.listdir(directory))
    print( random_image)
    await update.message.reply_photo(photo=directory + random_image, caption='🖐️👈')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    chat_id = update.message.chat_id
    text = update.message.text

    match text:
        case '1917':
            # await update.message.reply_sticker(sticker='CAACAgQAAxkBAAEo_sZlqq6-R7vS1YSrXccKtGwwcoTK7wACPxgAAqbxcR4lSV03aK6BaTQE')
            await update.message.reply_photo(photo='https://d15lrsitp7y7u.cloudfront.net/wp-content/uploads/2016/06/jordan-shrug-game.jpg', caption='GOAT🐐🐐🐐')
        case 'iris':
            await update.message.reply_sticker(sticker='CAACAgIAAxkBAAEo_qJlqqls0F4UzT-B-W3kTzb5FH3CuAACdRoAAgb-aUnKEzbSS0rckTQE')
        case 'timoxa':
            await update.message.reply_sticker(sticker='CAACAgIAAxkBAAEo_sRlqq62er6e7wL0S79SnZ-GQrWevQACMBkAAjalGUovXTYAAT6tdfk0BA')
        case 'medved':
            await update.message.reply_sticker(sticker='CAACAgIAAxkBAAEo_qRlqqlwYYUIDXLIPV1Jyfgo3iu46QAC9hgAArxzuEmjv6WqccYocDQE')
        case 'amir':
            await update.message.reply_sticker(sticker='CAACAgIAAxkBAAEo_qRlqqlwYYUIDXLIPV1Jyfgo3iu46QAC9hgAArxzuEmjv6WqccYocDQE')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6899842187:AAGzgwhea7dTAv0QiXJJegS8oUHbeVs4PkQ").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("daily_lebron", lebron_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()