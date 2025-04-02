from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from utils.error_handling import error_handler
from config_data.config import Config, load_config
from anketa_question.questions import dict_questions
from keyboards.anketa_keyboard import keyboard_anketa
from utils.send_admins import send_text_admins
from services.googlesheets import append_order
from database.models import User
from database.requests.rq_user import get_user_tg_id, update_user_organization

import logging

router = Router()
router.message.filter(F.chat.type == "private")
config: Config = load_config()


class Question(StatesGroup):
    question = State()


@router.message(F.text == 'Внести данные в регистр')
@error_handler
async def process_start_anketa(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем ответ на вопрос
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_start_anketa')
    user_info: User = await get_user_tg_id(tg_id=message.from_user.id)
    if user_info.organization == 'none':
        question = dict_questions[1]
        await state.update_data(answer=[])
        if question['list_buttons']:

            await message.answer(text=f"{question['message']}",
                                 reply_markup=keyboard_anketa(list_answer=question['list_buttons'],
                                                              count_question=1))
        else:
            await message.answer(text=f"{question['message']}")
            await state.set_state(Question.question)
    else:
        question = dict_questions[2]
        await state.update_data(answer=[f"-1_{user_info.organization}"])
        if question['list_buttons']:

            await message.answer(text=f"{question['message']}",
                                 reply_markup=keyboard_anketa(list_answer=question['list_buttons'],
                                                              count_question=2))
        else:
            await message.answer(text=f"{question['message']}")
            await state.set_state(Question.question)


@router.message(F.text, StateFilter(Question.question))
@error_handler
async def get_answer_question(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Получаем ответ на вопрос
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_answer_question ')
    data = await state.get_data()
    answer_list = data['answer']
    answer_list.append(f'-1_{message.text}')
    if len(dict_questions) == len(answer_list):
        text = f'Пользователь <a href="tg://userid?id={message.from_user.id}">{message.from_user.username}</a> ' \
               f'ответил на вопросы анкеты:\n\n'
        google_sheets_order = []
        for k, v in dict_questions.items():
            answer_item = answer_list[k-1].split('_', maxsplit=1)
            answer = answer_item[-1]
            if answer_item[0] != '-1':
                index = int(answer_item[0])
                answer = v["list_buttons"][index]
            google_sheets_order.append(answer)
            text += f'<b>{k}. {v["message"]}</b>\n' \
                    f'{answer}\n\n'
        await send_text_admins(bot=bot, text=text)
        append_order(order=google_sheets_order)
        await state.clear()
        await message.answer(text='Спасибо за уделенное время!')
        return

    await state.update_data(answer=answer_list)
    count_question = len(answer_list) + 1
    questions = dict_questions[count_question]
    if questions['list_buttons']:
        try:
            await message.edit_text(text=f"{questions['message']}",
                                    reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                 count_question=count_question))
        except:
            await message.answer(text=f"{questions['message']}",
                                 reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                              count_question=count_question))
        await state.set_state(state=None)
    else:
        try:
            await message.edit_text(text=f"{questions['message']}",
                                    reply_markup=None)
        except:
            await message.answer(text=f"{questions['message']}",
                                 reply_markup=None)
        await state.set_state(Question.question)


@router.callback_query(F.data.startswith('question'))
async def process_select_answer(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Возврат в начало бота
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_select_answer ')
    count_question = int(callback.data.split('_')[-1]) + 1
    print(count_question)
    if count_question == 2:
        await update_user_organization(tg_id=callback.from_user.id,
                                       organization=dict_questions[1]["list_buttons"][int(callback.data.split('_')[-2])])
    data = await state.get_data()
    answer_list = data['answer']
    answer_list.append(f"{callback.data.split('_')[-2]}_{count_question - 1}")
    if len(dict_questions) == count_question:

        text = f'Пользователь <a href="tg://user?id={callback.from_user.id}">{callback.from_user.username}</a> ' \
               f'ответил на вопросы анкеты:\n\n'
        google_sheets_order = []
        for k, v in dict_questions.items():
            answer_item = answer_list[k - 1].split('_', maxsplit=1)
            answer = answer_item[-1]
            if answer_item[0] != '-1':
                index = int(answer_item[0])
                answer = v["list_buttons"][index]
            google_sheets_order.append(answer)
            text += f'<b>{k}. {v["message"]}</b>\n' \
                    f'{answer}\n\n'
        await send_text_admins(bot=bot, text=text)
        append_order(order=google_sheets_order)
        await state.clear()
        await callback.message.answer(text='Спасибо за уделенное время!')
    else:
        await state.update_data(answer=answer_list)
        questions = dict_questions[count_question]
        if questions['list_buttons']:
            try:
                await callback.message.edit_text(text=f"{questions['message']}",
                                                 reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                              count_question=count_question))
            except:
                await callback.message.answer(text=f"{questions['message']}",
                                              reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                           count_question=count_question))
        else:
            try:
                await callback.message.edit_text(text=f"{questions['message']}",
                                                 reply_markup=None)
            except:
                await callback.message.answer(text=f"{questions['message']}",
                                              reply_markup=None)
            await state.set_state(Question.question)
    await callback.answer()
