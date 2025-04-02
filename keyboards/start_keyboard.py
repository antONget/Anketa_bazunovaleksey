from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import logging


def keyboard_start() -> ReplyKeyboardMarkup:
    """
    Стартовая клавиатура
    :return:
    """
    logging.info("keyboard_start")
    button_1 = KeyboardButton(text='Внести данные в регистр')
    button_2 = KeyboardButton(text='Информация о регистре')
    button_3 = KeyboardButton(text='Контакты')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2], [button_3]], resize_keyboard=True)
    return keyboard
