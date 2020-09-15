from telegram import Update
from telegram.ext import CallbackContext
from logger import logger_check_func
from database.models_users import DataBase_users

INFORM_FOR_USER = []

@logger_check_func
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome!!! Please write \
                                                                  comfortable time to get new words, please write"
                                                                  " like this (Example: 00:10, 11:23, 20:00)")
@logger_check_func
def get_info(update: Update, context: CallbackContext):
    text = update.message.text

    if len(str(text)) != 5 or text[2] != ':' or (int(text[:2]) > 23 or int(text[:2]) < 0)\
                                                or (int(text[3:]) > 59 or int(text[3:]) < 0):
        context.bot.send_message(chat_id=update.message.chat_id, text="Wrong, please write correctly time")

        return True
    else:
        INFORM_FOR_USER.append(update.message.chat_id)
        INFORM_FOR_USER.append(text)
        print(INFORM_FOR_USER)
        return False


