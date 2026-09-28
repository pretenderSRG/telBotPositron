import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import settings
from utils.logger_config import setup_logging
from handlers import routers

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands([
        BotCommand(command="start", description="Головне меню"),
        BotCommand(command="help", description="Допомога"),
        BotCommand(command="random", description="Випадковий факт"),
        BotCommand(command="gpt", description="Питання до ChatGPT"),
        BotCommand(command="talk", description="Діалог з відомою особистістю"),
        BotCommand(command="quiz", description="Квіз"),
    ])


async def main():
    setup_logging()
    settings.validate()

    bot = Bot(
        settings.BOT_API_KEY,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    await set_commands(bot)

    dp.include_routers(*routers)

    print("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Зупинка бота...")
