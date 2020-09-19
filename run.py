from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import Updater
from telegram.ext import Filters
from handler.commands import start, get_info, keyboard_callback_handler
from config import TG_TOKEN, TG_API_URL
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TIME, COUNT_WORDS = 1, 2

def bot_run():
    updater = Updater(token=TG_TOKEN, base_url=TG_API_URL, use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],
        states={
            TIME: [
                MessageHandler(Filters.text, get_info, pass_user_data=True),
            ],
            COUNT_WORDS: [
                CallbackQueryHandler(keyboard_callback_handler, pass_user_data=True, pass_job_queue=True)
            ]
        },
        fallbacks=[]
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)

    # Jobs Check
    #updater.job_queue.run_repetating(maker, interval='', first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    bot_run()