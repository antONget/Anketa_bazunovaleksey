from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from handlers import other_handlers, start_handlers, error
from handlers import anketa_handlers, command_handler
from database.models import async_main
from notify_admins import on_startup_notify

import asyncio
import logging

logger = logging.getLogger(__name__)


async def main():
    await async_main()
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    await on_startup_notify(bot=bot)
    dp.include_router(error.router)
    dp.include_router(start_handlers.router)
    dp.include_router(command_handler.router)
    dp.include_router(anketa_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся update и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

