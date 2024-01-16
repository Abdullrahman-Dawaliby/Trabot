
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from googletrans import Translator

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

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("6317504215:AAHG_W9IFQJZ8ZxAh8JLHkI_6JEuTbYt1Pk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the /start command handler
    dp.add_handler(CommandHandler("start", start))

    # Register a message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()