import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_anketa(list_answer: list[str], count_question: int) -> InlineKeyboardMarkup | None:
    """
    Клавиатура для ответа на вопросы
    :param list_answer:
    :param count_question:
    :return:
    """
    logging.info('keyboard_anketa')
    if list_answer:
        button = []
        for i, answer in enumerate(list_answer):
            button.append([InlineKeyboardButton(text=answer, callback_data=f'question_{i}_{count_question}')])
        keyboard = InlineKeyboardMarkup(inline_keyboard=button)
        return keyboard
    else:
        return None
