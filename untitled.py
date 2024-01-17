
import logging
import requests
import threading
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Welcome to the Telegram translator bot! Send me a message, and I will translate it for you.')

# Define a function to handle incoming messages and to translate them
def translate_message(update, context):
    # Get the message text
    message = update.message.text
    # Create a translator object
    translator = Translator()
    # Detect the language of the input message
    detected_language = translator.detect(message)
    # Translate the message to English
    translated_message = translator.translate(message, dest='en')
    # Reply with the translated message
    update.message.reply_text(f'Translated from {detected_language.lang} to English: {translated_message.text}')

# Function to send a keep-alive request to the Telegram API
def send_keep_alive_request(updater):
    updater.bot.get_me()  # Simple method call to keep the bot alive
    logger.info('Keep-alive request sent')

# Function to schedule the keep-alive request at regular intervals
def schedule_keep_alive_timer(updater, interval_in_seconds):
    while True:
        send_keep_alive_request(updater)
        time.sleep(interval_in_seconds)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("1639224318:AAHbzjwJ2rrGD3S6LQj23Wkos09pw9EoXhw", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the /start command handler
    dp.add_handler(CommandHandler("start", start))

    # Register a message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_message))

    # Start the Bot
    updater.start_polling()

    # Start the keep-alive timer
    keep_alive_interval = 3600  # 1 hour in seconds
    keep_alive_thread = threading.Thread(target=schedule_keep_alive_timer, args=(updater, keep_alive_interval))
    keep_alive_thread.start()

    updater.idle()

if __name__ == '__main__':
    main()
