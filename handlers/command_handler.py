import logging

from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import Command


from config_data.config import Config, load_config

router = Router()
config: Config = load_config()


@router.message(F.text == 'Информация о регистре')
async def command_help(message: Message, bot: Bot) -> None:
    """
    Помощь
    :param message:
    :param bot:
    :return:
    """
    logging.info('command_help')
    await message.answer(text="""Вся информация внесенная в данный регистр является конфиденциальной и не предоставляется для ознакомления третьим лицам.
Северо-западный TAVI регистр создан для мониторинга изменений в процедуре транскатетерной имплантации аортального клапана (TAVI). 
Цели создания регистра:
Исследование характеристик пациентов и процедуры TAVI. 
Поиск предикторов неблагоприятного прогноза после TAVI. 
Изучение оптимальной подходов в проведении процедуры TAVI.  
Возможность отслеживать, изменения процедуры TAVI, например, в плане упрощения, оптимизации и сокращения основных осложнений""")


@router.message(F.text == 'Связь с создателями')
async def command_support(message: Message, bot: Bot) -> None:
    """
    Поддержка
    :param message:
    :param bot:
    :return:
    """
    logging.info('command_support')
    await message.answer(text=f'Почта tavireregistry@gmail.com\n'
                              f'Телефон +7(911)822-72-66')
