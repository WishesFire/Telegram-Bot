from telegram import Update
from telegram import ParseMode
from telegram.ext import CallbackContext
from logger import logger_check_func
from keyboards.inline import get_base_inline_keyboard
from keyboards.inline import five_inline_keyboard, ten_inline_keyboard, fifteen_inline_keyboard
from database.models_users import DataBase_users

INFORM_FOR_USER = []
checker = True

@logger_check_func
def start(update: Update, context: CallbackContext):
    """
    /start
    """
    base = DataBase_users()
    check = base.user_check(update.message.chat_id)
    print(check)
    if not check:
        context.bot.send_message(chat_id=update.message.chat_id, text="\t<b>WELCOME MY FRIEND!!!</b>\n"
                                                                      "------------------------------------------------------------------\n"
                                                                      "Please write comfortable time😃 to get new words,"
                                                                      "please write like this 👉 <b>(Example: 00:10, 11:23, 20:00)</b>🙃",

                                 parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="<i>You are already in the system😃</i>",
                                 parse_mode=ParseMode.HTML)
    base.connect_close()

@logger_check_func
def get_info(update: Update, context: CallbackContext):
    """
    Get Information
    """
    global checker
    base = DataBase_users()
    check = base.user_check(update.message.chat_id)

    if checker and not check:
        text = update.message.text

        if len(str(text)) != 5 or text[2] != ':' or (int(text[:2]) > 23 or int(text[:2]) < 0)\
                                                    or (int(text[3:]) > 59 or int(text[3:]) < 0):
            context.bot.send_message(chat_id=update.message.chat_id, text="😡Wrong, please write correctly time😡")
            return True
        else:
            INFORM_FOR_USER.append(update.message.chat_id)
            INFORM_FOR_USER.append(text)
            context.bot.send_message(chat_id=update.message.chat_id, text="Thank you!!!👍")
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="<b>Choose how many words will be sent to you🎓</b>",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=get_base_inline_keyboard())

            checker = False
    base.connect_close()

def create_user():
    """
    Create user in DB
    """
    base = DataBase_users()
    base.push_date(INFORM_FOR_USER[0], INFORM_FOR_USER[1], INFORM_FOR_USER[2])
    base.connect_close()


@logger_check_func
def keyboard_callback_handler(update: Update, context: CallbackContext):
    """
    Words request handler
    """
    query = update.callback_query
    callback_data = query.data


    if callback_data == 'callback_five_words':
        query.edit_message_text(
            text=f"Cool...👌\n"
                 f"5 words will come in {INFORM_FOR_USER[1]}",
            reply_markup=five_inline_keyboard(),
        )
        INFORM_FOR_USER.append(5)

    elif callback_data == 'callback_ten_words':
        query.edit_message_text(
            text=f"Cool...👌\n"
                 f"10 words will come in {INFORM_FOR_USER[1]}",
            reply_markup=ten_inline_keyboard(),
        )
        INFORM_FOR_USER.append(10)

    elif callback_data == 'callback_fifteen_words':
        query.edit_message_text(
            text=f"Cool...👌\n"
                 f"15 words will come in {INFORM_FOR_USER[1]}",
            reply_markup=fifteen_inline_keyboard(),
        )
        INFORM_FOR_USER.append(15)

    create_user()