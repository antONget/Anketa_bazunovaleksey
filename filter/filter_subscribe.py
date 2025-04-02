from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot

from config_data.config import load_config, Config

import logging

config: Config = load_config()


def keyboards_subscription():
    logging.info(f'keyboards_subscription')
    button_1 = InlineKeyboardButton(text='Я подписался', callback_data='subscription')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1]], )
    return keyboard


class ChannelProtect(Filter):
    async def __call__(self, message: Message, bot: Bot):
        u_status = await bot.get_chat_member(chat_id=config.tg_bot.channel_name, user_id=message.from_user.id)
        if isinstance(u_status, ChatMemberMember) or isinstance(u_status, ChatMemberAdministrator) \
                or isinstance(u_status, ChatMemberOwner):
            return True
        if isinstance(message, CallbackQuery):
            await message.answer('')
            await message.message.answer(text=f'Чтобы получать вознаграждения за приглашенных пользователей, а самому'
                                              f' найти вакансию своей мечты подпишись на канал '
                                              f'<a href="{config.tg_bot.channel_name}">'
                                              f'{config.tg_bot.channel_name}</a>',
                                         reply_markup=keyboards_subscription(),
                                         parse_mode='html')
        else:
            await message.answer(text=f'Чтобы получать вознаграждения за приглашенных пользователей, а самому найти'
                                      f' вакансию своей мечты подпишись на канал '
                                      f'<a href="{config.tg_bot.channel_name}">{config.tg_bot.channel_name}</a>',
                                 reply_markup=keyboards_subscription(),
                                 parse_mode='html')
        return False
