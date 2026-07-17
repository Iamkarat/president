import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.database.repository import init_db
from bot.handlers import get_root_router
from bot.utils.logger import setup_logging

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()
    logger.info("Запуск бота PRESIDENT")

    if not config.bot_token:
        raise RuntimeError("BOT_TOKEN не задан. Проверьте файл .env")

    await init_db()

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.include_router(get_root_router())

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
