import sys
import json
from telegram import Update
import pandas as pd
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from utilities.getSecrets import *
from utilities.redditPost import *


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def post_command(update: Update, context: CallbackContext) -> None:
    """Send a posts when the command /post is issued."""
    settingFile = open('settings.json')
    settings = json.load(settingFile)

    appClientId = get_secret(settings['appClientId'], settings['keyVaultName'])
    appSecret = get_secret(settings['appSecretName'], settings['keyVaultName'])
    redditUsername = get_secret(settings['redditUsername'], settings['keyVaultName'])
    redditPassword = get_secret(settings['redditPassword'], settings['keyVaultName'])

    header = authenticateReddit(appClientId, appSecret, redditUsername, redditPassword)
    posts = get_postData(header, settings['subreddits'])

    for post in posts:
        for i in post:
            for key, value in i.items():
                update.message.reply_text(f"{key}\n{value}\n---\n")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)
        
def main():
    settingFile = open('settings.json')
    settings = json.load(settingFile)

    botSecret = get_secret(settings['botSecretName'], settings['keyVaultName'])

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=botSecret, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("post", post_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
