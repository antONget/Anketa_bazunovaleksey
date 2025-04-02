from aiogram import Bot
from config_data.config import Config, load_config

config: Config = load_config()


async def send_text_admins(bot: Bot, text: str):
    """
    Рассылка сообщения администраторам
    :param bot:
    :param text:
    :return:
    """
    list_admins = config.tg_bot.admin_ids.split(',')
    n = 4000
    for admin in list_admins:
        for text_part in [text[i:i + n] for i in range(0, len(text), n)]:
            try:
                await bot.send_message(chat_id=admin,
                                       text=text_part)
            except:
                pass
