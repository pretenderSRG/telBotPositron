import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import Default, DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import settings
from handlers import router
from utils.logger_config import setup_logging


logger = logging.getLogger(__name__)

async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands([
        BotCommand(command="start", description="Розпочати"),
        BotCommand(command="gpt", description="Питання до ChatGPT"),
        BotCommand(command="random", description="Випадковий факт"),
        BotCommand(command="help", description="Справка"),
    ])


async def main():
    setup_logging()

    bot = Bot(settings.BOT_API_KEY,
             default=DefaultBotProperties(parse_mode=ParseMode.HTML), )
    dp = Dispatcher()

    await set_commands(bot)

    dp.include_routers(router)

    print("Запуск бота...")

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Зупинка бота...")
