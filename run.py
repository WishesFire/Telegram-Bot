from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import Filters
from handler.commands import start, get_info, keyboard_callback_handler
from config import TG_TOKEN, TG_API_URL
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
swapped = True

def bot_run():
    updater = Updater(token=TG_TOKEN, base_url=TG_API_URL, use_context=True)
    global swapped

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, get_info))
    dispatcher.add_handler(CallbackQueryHandler(keyboard_callback_handler))


    # Jobs Check
    #updater.job_queue.run_repetating(maker, interval='', first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    bot_run()