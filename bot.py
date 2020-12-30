from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def traders(update, context):
    with app.app_context():
        c = Trader.query.all()
        update.message.reply_text(json.dumps(c, cls=AlchemyEncoder))

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

updater = Updater("1427053944:AAEWTsalt2w0kmw-yKAK5qqIn_tAPxn7H-4", use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("traders", traders))
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_error_handler(error)
updater.start_polling()
updater.idle()
