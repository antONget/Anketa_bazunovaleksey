import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from database.requests import rq_user
from utils.error_handling import error_handler
from filter.admin_filter import check_super_admin
from config_data.config import Config, load_config
from keyboards.start_keyboard import keyboard_start

import logging

router = Router()
router.message.filter(F.chat.type == "private")
config: Config = load_config()


class SelectTeam(StatesGroup):
    team = State()


@router.message(CommandStart())
@error_handler
async def process_press_start(message: Message, state: FSMContext, command: CommandObject, bot: Bot) -> None:
    """
    Обработка нажатия на кнопку старт и вывод списка события
    :param message:
    :param state:
    :param command:
    :param bot:
    :return:
    """
    logging.info('process_press_start ')
    tg_id: int = message.from_user.id
    username: str = message.from_user.username
    data = {"tg_id": tg_id, "username": username}
    await rq_user.add_user(data)
    await message.answer(text='Добро пожаловать в Telegram-бот регистра TAVI!\n\n'
                              'С помощью этого бота вы сможете быстро и удобно заполнять регистрационную'
                              ' форму для заполнения.',
                         reply_markup=keyboard_start())


@router.callback_query(F.data == '/cancel')
async def process_select_action(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Возврат в начало бота
    :param callback:
    :param state:
    :param bot:
    :return:
    """
    await state.clear()

