import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from anketa_question.questions import dict_questions


def keyboard_anketa(list_answer: list[str], count_question: int, list_select: list = None) -> InlineKeyboardMarkup | None:
    """
    Клавиатура для ответа на вопросы
    :param list_answer:
    :param count_question:
    :param list_select:
    :return:
    """
    logging.info('keyboard_anketa')
    isMultiselect = dict_questions[count_question].get('multiselect')
    if list_answer:
        button = []
        button_continue = [InlineKeyboardButton(text='Далее',
                                                callback_data=f'continue_{count_question}')]
        for i, answer in enumerate(list_answer):
            prefix_callback_data = f'question'
            select = ''
            if isMultiselect:
                prefix_callback_data = f'multiselect'
                select = ''
            if isMultiselect and list_select:
                if answer in list_select:
                    select = '✅'
            button.append([InlineKeyboardButton(text=f'{select} {answer}',
                                                callback_data=f'{prefix_callback_data}_{i}_{count_question}')])
        if isMultiselect:
            button.append(button_continue)
        keyboard = InlineKeyboardMarkup(inline_keyboard=button)
        return keyboard
    else:
        return None


def keyboard_39(count_question: int) -> InlineKeyboardMarkup:
    """
    ['Тип 1',
   'Тип 2',
   'Тип 3']
    :return:
    """
    logging.info('keyboard_40')
    button_1 = InlineKeyboardButton(text='Тип 1',
                                    callback_data=f'other_question_0_{count_question - 1}')
    button_2 = InlineKeyboardButton(text='Тип 2',
                                    callback_data=f'other_question_1_{count_question - 1}')
    button_3 = InlineKeyboardButton(text='Тип 3',
                                    callback_data=f'other_question_2_{count_question - 1}')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2], [button_3]],
    )
    return keyboard


def keyboard_46(other_select_list: list, count_question: int) -> InlineKeyboardMarkup:
    """
    ['Главный ствол ЛКА',
   'Передняя межжелудочковая артерия',
   'Огибающая артерия',
   'Правая коронарная артерия']
    :return:
    """
    logging.info('keyboard_46')

    button_list = []
    print(other_select_list)
    for i, text in enumerate(['Главный ствол ЛКА', 'Передняя межжелудочковая артерия', 'Огибающая артерия', 'Правая коронарная артерия']):
        select = ''
        if text in other_select_list:
            select = "✅"
        button_list.append([InlineKeyboardButton(text=f'{select} {text}',
                                                 callback_data=f'other_question_{i}_{count_question - 1}')])

    button_continue = [InlineKeyboardButton(text='Далее',
                                            callback_data=f'continue_{count_question - 1}')]
    button_list.append(button_continue)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=button_list,
    )
    return keyboard


def keyboard_53(other_select_list: list, count_question: int) -> InlineKeyboardMarkup:
    """
    ['Восходящая аорта',
     'Дуга аорты',
     'Грудная аорта',
     'Брюшная аорта']
    :return:
    """
    logging.info('keyboard_53')
    button_list = []
    for i, text in enumerate(['Восходящая аорта', 'Дуга аорты', 'Грудная аорта', 'Брюшная аорта']):
        select = ''
        if text in other_select_list:
            select = "✅"
        button_list.append([InlineKeyboardButton(text=f'{select} {text}',
                                                 callback_data=f'other_question_{i}_{count_question - 1}')])

    button_continue = [InlineKeyboardButton(text='Далее',
                                            callback_data=f'continue_{count_question - 1}')]
    button_list.append(button_continue)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=button_list,
    )
    return keyboard

# def keyboard_53() -> InlineKeyboardMarkup:
#     """
#      ['Восходящая аорта',
#      'Дуга аорты',
#      'Грудная аорта',
#      'Брюшная аорта']
#     :return:
#     """
#     logging.info('keyboard_40')
#     button_1 = InlineKeyboardButton(text='Восходящая аорта',
#                                     callback_data='other_question_0')
#     button_2 = InlineKeyboardButton(text='Дуга аорты',
#                                     callback_data='other_question_1')
#     button_3 = InlineKeyboardButton(text='Грудная аорта',
#                                     callback_data='other_question_2')
#     button_4 = InlineKeyboardButton(text='Брюшная аорта',
#                                     callback_data='other_question_3')
#     button_continue = InlineKeyboardButton(text='Далее',
#                                            callback_data='other_continue')
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_continue]],
#     )
#     return keyboard


def keyboard_64_Medtronic(count_question: int) -> InlineKeyboardMarkup:
    """
      ['CoreValve',
     'Evolut R',
     'Evolut Pro',
     'Evolut Pro+']
    :return:
    """
    logging.info('keyboard_68_Medtronic')
    button_1 = InlineKeyboardButton(text='CoreValve',
                                    callback_data=f'other_question_0_{count_question - 1}')
    button_2 = InlineKeyboardButton(text='Evolut R',
                                    callback_data=f'other_question_1_{count_question - 1}')
    button_3 = InlineKeyboardButton(text='Evolut Pro',
                                    callback_data=f'other_question_2_{count_question - 1}')
    button_4 = InlineKeyboardButton(text='Evolut Pro+',
                                    callback_data=f'other_question_3_{count_question - 1}')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2], [button_3], [button_4]],
    )
    return keyboard


def keyboard_64_Abbott(count_question: int) -> InlineKeyboardMarkup:
    """
      ['PORTICO',
      'Navitor']
    :return:
    """
    logging.info('keyboard_68_Abbott')
    button_1 = InlineKeyboardButton(text='PORTICO',
                                    callback_data=f'other_question_0_{count_question - 1}')
    button_2 = InlineKeyboardButton(text='Navitor',
                                    callback_data=f'other_question_1_{count_question - 1}')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2]],
    )
    return keyboard


def keyboard_64_Boston_Scientific(count_question: int) -> InlineKeyboardMarkup:
    """
      ['AСURATE neo',
       'AСURATE neo2']
    :return:
    """
    logging.info('keyboard_68_Boston_Scientific')
    button_1 = InlineKeyboardButton(text='AСURATE neo',
                                    callback_data=f'other_question_0_{count_question - 1}')
    button_2 = InlineKeyboardButton(text='AСURATE neo2',
                                    callback_data=f'other_question_1_{count_question - 1}')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2]],
    )
    return keyboard


def keyboard_72(count_question: int) -> InlineKeyboardMarkup:
    """
      ['Реканализация, стентирование',
                'Реканализация, баллонная ангиопластика',
                'Коронарное шунтирование']
    :return:
    """
    logging.info('keyboard_72')
    button_1 = InlineKeyboardButton(text='Реканализация, стентирование',
                                    callback_data=f'other_question_0_{count_question - 1}')
    button_2 = InlineKeyboardButton(text='Реканализация, баллонная ангиопластика',
                                    callback_data=f'other_question_1_{count_question - 1}')
    button_3 = InlineKeyboardButton(text='Коронарное шунтирование',
                                    callback_data=f'other_question_2_{count_question - 1}')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2], [button_3]],
    )
    return keyboard


def keyboard_74(count_question: int) -> InlineKeyboardMarkup:
    """
      ['PROSTAR',
      '2x ProGlide',
      'ProGlide и Angio-Seal']
    :return:
    """
    logging.info('keyboard_74')
    button_1 = InlineKeyboardButton(text='PROSTAR',
                                    callback_data=f'other_question_0_{count_question - 1}')
    button_2 = InlineKeyboardButton(text='2x ProGlide',
                                    callback_data=f'other_question_1_{count_question - 1}')
    button_3 = InlineKeyboardButton(text='ProGlide и Angio-Seal',
                                    callback_data=f'other_question_2_{count_question - 1}')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2], [button_3]],
    )
    return keyboard
