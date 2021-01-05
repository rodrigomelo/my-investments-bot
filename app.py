import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi!')

def help(update, context):
    update.message.reply_text('Help!')

def countries(update, context):
    response = requests.get("http://127.0.0.1:5000/api/countries")
    update.message.reply_text(response.json())

def traders(update, context):
    response = requests.get("http://127.0.0.1:5000/api/traders")
    update.message.reply_text(response.json())

def trades(update, context):
    response = requests.get("http://127.0.0.1:5000/api/trades")
    update.message.reply_text(response.json())

def echo(update, context):
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater("1427053944:AAEWTsalt2w0kmw-yKAK5qqIn_tAPxn7H-4", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("countries", countries))
    dp.add_handler(CommandHandler("traders", traders))
    dp.add_handler(CommandHandler("trades", trades))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
