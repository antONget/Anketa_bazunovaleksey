from aiogram.types import CallbackQuery
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from handlers.anketa_handlers import Question
import logging


async def other_answer_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Изменяем логику анкеты
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('other_answer_callback')
    data = await state.get_data()
    other_answer = data['other_answer']
    count_question = data['count_question']
    if count_question == 17:
        await callback.message.edit_text(text='Дата и название операции')
        await state.set_state(Question.question)