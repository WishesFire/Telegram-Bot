from telegram import Update
from telegram import ParseMode
from telegram.ext import CallbackContext, ConversationHandler
from logger import logger_check_func
from keyboards.inline import get_base_inline_keyboard, get_base_reply_keyboard
from keyboards.inline import five_inline_keyboard, ten_inline_keyboard, fifteen_inline_keyboard
from database.models_users import DataBase_users
from database.models_words import DataBase_words
import time
from datetime import timedelta

TIME, COUNT_WORDS = 1, 2
base = DataBase_users()
wordest = DataBase_words()

@logger_check_func
def start(update: Update, context: CallbackContext):
    """
    /start
    """
    check = base.user_check(update.message.chat_id)
    if not check:
        context.bot.send_message(chat_id=update.message.chat_id, text="\t<b>WELCOME MY FRIEND!!!</b>\n"
                                                                      "------------------------------------------------------------------\n"
                                                                      "Please write comfortable time😃 to get new words,"
                                                                      "please write like this 👉 <b>(Example: 00:10, 11:23, 20:00)</b>🙃",

                                 parse_mode=ParseMode.HTML, reply_markup=get_base_reply_keyboard())
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="<i>You are already in the system😃</i>",
                                 parse_mode=ParseMode.HTML)
    return TIME

@logger_check_func
def get_time(update: Update, context: CallbackContext):
    check = base.user_check(update.message.chat_id)
    time_now = current_time()

    if not check:
        context.bot.send_message(chat_id=update.message.chat_id, text='You are not in the system😃')
    else:
        time_user = str(base.get_user_time(update.message.chat_id))[2:7]
        cur_hour = timedelta(hours=int(time_now[0:2]), minutes=int(time_now[3:]))
        cur_minutes = timedelta(hours=int(time_user[0:2]), minutes=int(time_user[3:]))
        final_times = cur_minutes - cur_hour
        context.bot.send_message(chat_id=update.message.chat_id, text=str(final_times))


def current_time():
    time_now = time.localtime()[3:5]

    if len(str(time_now[1])) != 2:  # Проверка на 0
        time_now = f"{time_now[0]}:0{time_now[1]}"
    elif len(str(time_now[0])) != 2:
        time_now = f"0{time_now[0]}:{time_now[1]}"
    else:
        time_now = f"{time_now[0]}:{time_now[1]}"

    return time_now


@logger_check_func
def get_info(update: Update, context: CallbackContext):
    """
    Get Information
    """
    text = update.message.text
    check = base.user_check(update.message.chat_id)

    if not check:
        if len(str(text)) != 5 or text[2] != ':' or (int(text[:2]) > 23 or int(text[:2]) < 0)\
                                                        or (int(text[3:]) > 59 or int(text[3:]) < 0):
            context.bot.send_message(chat_id=update.message.chat_id, text="😡Wrong, please write correctly time😡")

        else:
            context.user_data[TIME] = text
            context.bot.send_message(chat_id=update.message.chat_id, text="Thank you!!!👍")
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="<b>Choose how many words will be sent to you🎓</b>",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=get_base_inline_keyboard())

            return COUNT_WORDS

    elif check and base.get_using_set(update.message.chat_id) == 0:
        if len(str(text)) != 5 or text[2] != ':' or (int(text[:2]) > 23 or int(text[:2]) < 0)\
                                                        or (int(text[3:]) > 59 or int(text[3:]) < 0):
            context.bot.send_message(chat_id=update.message.chat_id, text="😡Wrong, please write correctly time😡")

        else:
            base.change_data(update.message.chat_id, text)
            context.bot.send_message(chat_id=update.message.chat_id, text="Thank you!!!👍")
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="<b>Choose how many words will be sent to you🎓</b>",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=get_base_inline_keyboard())

            return COUNT_WORDS


    elif text == 'Write /start and after click button' and check:
        base.change_using_set(update.message.chat_id, 0)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="You chose settings, please write your new time and number of words",
                                 parse_mode=ParseMode.HTML)
        return TIME

    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="<i>You are already in the system😃</i>",
                                 parse_mode=ParseMode.HTML)

@logger_check_func
def keyboard_callback_handler(update: Update, context: CallbackContext):
    """
    Words request handler
    """
    check = base.user_check(update.callback_query.message.chat.id)
    if not check:
        query = update.callback_query
        callback_data = query.data

        if callback_data == 'callback_five_words':
            query.edit_message_text(
                text=f"Cool...👌\n"
                     f"5 words will come to you",
                reply_markup=five_inline_keyboard(),
            )
            context.user_data[COUNT_WORDS] = 5


        elif callback_data == 'callback_ten_words':
            query.edit_message_text(
                text=f"Cool...👌\n"
                     f"10 words will come to you",
                reply_markup=ten_inline_keyboard(),
            )
            context.user_data[COUNT_WORDS] = 10


        elif callback_data == 'callback_fifteen_words':
            query.edit_message_text(
                text=f"Cool...👌\n"
                     f"15 words will come to you",
                reply_markup=fifteen_inline_keyboard(),
            )
            context.user_data[COUNT_WORDS] = 15

        base.push_date(update.callback_query.message.chat.id, context.user_data[TIME], context.user_data[COUNT_WORDS])
        context.user_data.clear()
        context.job_queue.run_repeating(jobolin, interval=60, context=update.callback_query.message.chat.id)

        return ConversationHandler.END

    elif base.get_using_set(update.callback_query.message.chat.id) == 0:
        query = update.callback_query
        callback_data = query.data

        if callback_data == 'callback_five_words':
            query.edit_message_text(
                text=f"Cool...👌\n"
                     f"5 words will come to you",
                reply_markup=five_inline_keyboard(),
            )
            base.change_count(update.callback_query.message.chat.id, 5)


        elif callback_data == 'callback_ten_words':
            query.edit_message_text(
                text=f"Cool...👌\n"
                     f"10 words will come to you",
                reply_markup=ten_inline_keyboard(),
            )
            base.change_count(update.callback_query.message.chat.id, 10)


        elif callback_data == 'callback_fifteen_words':
            query.edit_message_text(
                text=f"Cool...👌\n"
                     f"15 words will come to you",
                reply_markup=fifteen_inline_keyboard(),
            )
            base.change_count(update.callback_query.message.chat.id, 15)

        context.user_data.clear()
        base.change_using_set(update.callback_query.message.chat.id, 1)
        return ConversationHandler.END

def jobolin(context: CallbackContext):
    lst_all_time = base.user_for_time(context.job.context) # ПРОВЕРКА!!!
    time_now = current_time()

    if time_now == lst_all_time[0]:
        five_randon = wordest.request_random_word(lst_all_time[1])
        for i in five_randon:
            context.bot.send_message(chat_id=context.job.context, text=f'<b>English word     Russion Translate</b>\n\n '
                                                                       f'{i[0]}-{i[1]}',
                                     parse_mode=ParseMode.HTML)