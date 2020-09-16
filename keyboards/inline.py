from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton


def get_base_inline_keyboard():
    """
    Keyboard button
    """
    keyboard = [
        [
            InlineKeyboardButton('5 Words👻', callback_data='callback_five_words'),
            InlineKeyboardButton('10 Words👽', callback_data='callback_ten_words'),
            InlineKeyboardButton('15 Words🤖', callback_data='callback_fifteen_words'),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)

def five_inline_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton('5 Words👻', callback_data='callback_five__words')]])

def ten_inline_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton('10 Words👽', callback_data='callback_ten__words')]])

def fifteen_inline_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton('15 Words🤖', callback_data='callback_fifteen__words')]])