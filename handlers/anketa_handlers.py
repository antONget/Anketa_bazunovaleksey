from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from utils.error_handling import error_handler
from config_data.config import Config, load_config
from anketa_question.questions import dict_questions
from anketa_question.other_question import other_question
from keyboards.anketa_keyboard import keyboard_anketa, keyboard_39, keyboard_46, keyboard_53, keyboard_64_Medtronic, \
    keyboard_64_Abbott, keyboard_64_Boston_Scientific, keyboard_72, keyboard_74
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
async def process_start_questionnaire(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запускаем анкетирование
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_start_anketa')
    user_info: User = await get_user_tg_id(tg_id=message.from_user.id)
    await state.update_data(answer=[])
    await state.update_data(multiselect=[])
    # если пользователь еще не отвечал на первый вопрос
    if user_info.organization == 'none':
        question = dict_questions[1]
        if question['list_buttons']:
            await message.answer(text=f"{question['message']}",
                                 reply_markup=keyboard_anketa(list_answer=question['list_buttons'],
                                                              count_question=1))
        else:
            await message.answer(text=f"{question['message']}")
            await state.set_state(Question.question)
    # если пользователь уже отвечал на опросник
    else:
        question = dict_questions[2]
        await state.update_data(answer=[f"{user_info.organization}"])
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
    Получаем ответ на вопрос требующий ввода пользователя
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('get_answer_question ')
    data = await state.get_data()
    answer_list = data['answer']
    # вопросы требующие отдельной логики
    if (len(answer_list) + 1) in [16, 25, 29, 39, 46, 53, 64, 72, 74]:
        answer_list.append([data['other_answer'], message.text])
    else:
        # заносим ответ в список без отдельной логики
        answer_list.append(message.text)
    print("Номер вопроса:", len(answer_list))
    print("Список ответов:", answer_list)
    # если количество вопросов = количеству ответов
    if len(dict_questions) == len(answer_list):
        # text = f'Пользователь <a href="tg://userid?id={message.from_user.id}">{message.from_user.username}</a> ' \
        #        f'ответил на вопросы анкеты:\n\n'
        # google_sheets_order = []
        # for k, v in dict_questions.items():
        #     answer_item = answer_list[k-1].split('_', maxsplit=1)
        #     answer = answer_item[-1]
        #     if answer_item[0] != '-1':
        #         index = int(answer_item[0])
        #         answer = v["list_buttons"][index]
        #     google_sheets_order.append(answer)
        #     text += f'<b>{k}. {v["message"]}</b>\n' \
        #             f'{answer}\n\n'
        # await send_text_admins(bot=bot, text=text)
        # # append_order(order=google_sheets_order)
        # await state.clear()
        # await message.answer(text='Благодарим за внесение ваших данных!\n'
        #                           'Ждем новых кейсов!\n'
        #                           'Желаем удачных имплантаций!')
        await process_finish_questionnaire(answer_list=answer_list, message=message, state=state, bot=bot)
        return

    # увеличиваем номер вопроса на один для вывода следующего вопроса
    await state.update_data(answer=answer_list)
    count_question = len(answer_list) + 1
    questions = dict_questions[count_question]
    # если у вопроса есть варианты для выбора
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
    # если у вопроса нет вариантов для выбора
    else:
        try:
            await message.edit_text(text=f"{questions['message']}",
                                    reply_markup=None)
        except:
            await message.answer(text=f"{questions['message']}",
                                 reply_markup=None)
        await state.set_state(Question.question)


@router.callback_query(F.data.startswith('question'))
@router.callback_query(F.data.startswith('continue'))
@router.callback_query(F.data.startswith('other_question'))
@router.callback_query(F.data.startswith('other_continue'))
async def process_select_answer(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Получаем выбор
    :param callback: question_{i}_{count_question}, continue_{count_question}
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_select_answer')
    print(callback.data)
    count_question = int(callback.data.split('_')[-1]) + 1
    if (count_question - 1) in [16, 25, 29, 39, 46, 53, 64, 72, 74] and \
            (callback.data.startswith('question') or callback.data.startswith('continue')):
        await state.update_data(count_question=count_question)
        if (count_question - 1 == 16 or count_question - 1 == 25 or count_question - 1 == 29 or
            count_question - 1 == 39 or count_question - 1 == 46 or count_question - 1 == 53 or
            count_question - 1 == 72 or count_question - 1 == 74) \
                and (callback.data.split('_')[-2] == '1' or callback.data.split('_')[0] == 'continue'):
            pass
        elif count_question - 1 == 64 and callback.data.split('_')[-2] not in ['0', '1', '2']:
            pass
        else:
            await other_answer_callback(callback=callback, state=state, bot=bot)
            return
        # if count_question - 1 == 16 and \
        #    dict_questions[count_question-1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Да':
        #     await state.update_data(count_question=count_question)
        #     await state.update_data(
        #         other_answer=[f"{dict_questions[count_question-1]['list_buttons'][int(callback.data.split('_')[-2])]}"])
        #     await other_answer_callback(callback=callback, state=state, bot=bot)
        #     return


    print("Номер вопроса:", count_question-1)
    # !!! раскомментировать
    if count_question == 2:
        await update_user_organization(tg_id=callback.from_user.id,
                                       organization=dict_questions[1]["list_buttons"][int(callback.data.split('_')[-2])])
    data = await state.get_data()
    answer_list = data['answer']
    # добавляем выбор на линейный вопрос
    if callback.data.split('_')[0] == 'question':
        answer_list.append(f"{dict_questions[count_question-1]['list_buttons'][int(callback.data.split('_')[-2])]}")
    # если был выбран вариант нелинейного вопроса
    elif callback.data.split('_')[0] == 'other':
        other_answer_id: int = int(callback.data.split('_')[-2])
        if other_question[count_question-1].get('multiselect'):
            multiselect: list = data['multiselect']
            print(other_answer_id, multiselect[0], count_question-1)
            answer = other_question[count_question-1][multiselect[0]][other_answer_id]
            if answer in multiselect:
                multiselect.remove(answer)
            else:
                multiselect.append(answer)
            if count_question-1 == 46:
                try:
                    await callback.message.edit_text(
                        text='Укажите пораженные коронарные артерии (Возможность множественного выбора)',
                        reply_markup=keyboard_46(other_select_list=multiselect, count_question=count_question))
                except:
                    await callback.message.edit_text(
                        text='Укажите пораженные коронарные артерии (Возможность множественного выбора).',
                        reply_markup=keyboard_46(other_select_list=multiselect, count_question=count_question))
                return
            if count_question-1 == 53:
                try:
                    await callback.message.edit_text(
                        text='Указать отдел аорты (Возможность множественного выбора',
                        reply_markup=keyboard_53(other_select_list=multiselect, count_question=count_question))
                except:
                    await callback.message.edit_text(
                        text='Указать отдел аорты (Возможность множественного выбора.',
                        reply_markup=keyboard_53(other_select_list=multiselect, count_question=count_question))
                return
        if callback.data.startswith('other_question'):
            other_answer: list = data['other_answer']
            other_answer.append(other_question[count_question-1][other_answer[0]][other_answer_id])
        answer_list.append(other_answer)
        await state.update_data(other_answer=[])
    # получение выбора на мультиселектный вопрос
    else:
        answer_list.append(data['multiselect'])
        await state.update_data(multiselect=[])
    print("Список ответов:", answer_list)
    if len(dict_questions) == count_question:
        await process_finish_questionnaire(answer_list=answer_list, message=callback.message, state=state, bot=bot)
        # text = f'Пользователь <a href="tg://user?id={callback.from_user.id}">{callback.from_user.username}</a> ' \
        #        f'ответил на вопросы анкеты:\n\n'
        # google_sheets_order = []
        # for k, v in dict_questions.items():
        #     answer_item = answer_list[k - 1].split('_', maxsplit=1)
        #     answer = answer_item[-1]
        #     if answer_item[0] != '-1':
        #         index = int(answer_item[0])
        #         answer = v["list_buttons"][index]
        #     google_sheets_order.append(answer)
        #     text += f'<b>{k}. {v["message"]}</b>\n' \
        #             f'{answer}\n\n'
        # await send_text_admins(bot=bot, text=text)
        # append_order(order=google_sheets_order)
        # await state.clear()
        # await callback.message.answer(text='Благодарим за внесение ваших данных!\n'
        #                                    'Ждем новых кейсов!\n'
        #                                    'Желаем удачных имплантаций!')

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
            await state.set_state(state=None)
        else:
            try:
                await callback.message.edit_text(text=f"{questions['message']}",
                                                 reply_markup=None)
            except:
                await callback.message.answer(text=f"{questions['message']}",
                                              reply_markup=None)
            await state.set_state(Question.question)
    await callback.answer()


@router.callback_query(F.data.startswith('multiselect'))
async def process_select_answer(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Возврат в начало бота
    :param callback: {prefix_callback_data}_{i}_{count_question}
    :param state:
    :param bot:
    :return:
    """
    logging.info('process_select_answer ')
    count_question = int(callback.data.split('_')[-1])
    select_answer_id = int(callback.data.split('_')[-2])
    data = await state.get_data()
    multiselect: list = data['multiselect']
    answer = dict_questions[count_question]["list_buttons"][select_answer_id]
    if answer in multiselect:
        multiselect.remove(answer)
    else:
        multiselect.append(answer)
    questions = dict_questions[count_question]
    await state.update_data(multiselect=multiselect)
    print(multiselect)
    try:
        await callback.message.edit_text(text=f"{questions['message']}",
                                         reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                      count_question=count_question,
                                                                      list_select=multiselect))
    except:
        await callback.message.edit_text(text=f"{questions['message']}.",
                                         reply_markup=keyboard_anketa(list_answer=questions['list_buttons'],
                                                                      count_question=count_question,
                                                                      list_select=multiselect))


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
    count_question = data['count_question']
    if count_question - 1 == 16 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Да':
        await state.update_data(
            other_answer='Да')
        await callback.message.edit_text(text='Дата и название операции')
        await state.set_state(Question.question)
    if count_question - 1 == 25 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Да':
        await state.update_data(
            other_answer='Да')
        await callback.message.edit_text(text='Указать какие')
        await state.set_state(Question.question)
    if count_question - 1 == 29 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Да':
        await state.update_data(
            other_answer=['Да'])
        await callback.message.edit_text(text='Указать онкологический процесс')
        await state.set_state(Question.question)

    if count_question - 1 == 39 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Бикуспидальная анатомия':
        await callback.message.edit_text(text='Анатомическая характеристика бикуспидального АоК',
                                         reply_markup=keyboard_39(count_question=count_question))
        await state.update_data(
            other_answer=['Бикуспидальная анатомия'])

    if count_question - 1 == 46 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Да':
        await callback.message.edit_text(text='Укажите пораженные коронарные артерии (Возможность множественного выбора)',
                                         reply_markup=keyboard_46(other_select_list=[], count_question=count_question))
        await state.update_data(multiselect=['Да'])

    if count_question - 1 == 53 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Да':
        await callback.message.edit_text(text='Указать отдел аорты (Возможность множественного выбора)',
                                         reply_markup=keyboard_53(other_select_list=[], count_question=count_question))
        await state.update_data(multiselect=['Да'])

    if count_question - 1 == 64 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Medtronic':
        await callback.message.edit_text(text='Модель биопротеза Medtronic',
                                         reply_markup=keyboard_64_Medtronic(count_question=count_question))
        await state.update_data(other_answer=['Medtronic'])

    if count_question - 1 == 64 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Abbott':
        await callback.message.edit_text(text='Модель биопротеза Abbott',
                                         reply_markup=keyboard_64_Abbott(count_question=count_question))
        await state.update_data(other_answer=['Abbott'])

    if count_question - 1 == 64 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Boston Scientific':
        await callback.message.edit_text(text='Модель биопротеза Boston Scientific',
                                         reply_markup=keyboard_64_Boston_Scientific(count_question=count_question))
        await state.update_data(other_answer=['Boston Scientific'])

    if count_question - 1 == 72 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Да':
        await callback.message.edit_text(text='Способ восстановления кровотока по коронарным артериям',
                                         reply_markup=keyboard_72(count_question=count_question))
        await state.update_data(other_answer=['Да'])

    if count_question - 1 == 74 and \
            dict_questions[count_question - 1]['list_buttons'][int(callback.data.split('_')[-2])] == 'Эндоваскулярно (ушивающие устройства)':
        await callback.message.edit_text(text='Выбор ушивающих устройств',
                                         reply_markup=keyboard_74(count_question=count_question))
        await state.update_data(other_answer=['Эндоваскулярно (ушивающие устройства)'])


async def process_finish_questionnaire(answer_list: list, message: Message, state: FSMContext, bot: Bot):
    """
    Процесс завершения анкетирования
    :param answer_list:
    :param message:
    :param state:
    :param bot:
    :return:
    """
    # text = f'Пользователь <a href="tg://userid?id={message.from_user.id}">{message.from_user.username}</a> ' \
    #        f'ответил на вопросы анкеты:\n\n'
    google_sheets_order = []
    # for k, v in dict_questions.items():
    #     answer = answer_list[k-1]
    #     google_sheets_order.append(answer_list)
    #     text += f'<b>{k}. {v["message"]}</b>\n' \
    #             f'{answer}\n\n'
    # await send_text_admins(bot=bot, text=text)
    for item in answer_list:
        google_sheets_order.append(str(item))
    append_order(order=google_sheets_order)
    await state.clear()
    await message.answer(text='Благодарим за внесение ваших данных!\n'
                              'Ждем новых кейсов!\n'
                              'Желаем удачных имплантаций!')
