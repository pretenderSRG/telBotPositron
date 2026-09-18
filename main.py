import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import settings
from handlers import router


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands([
        BotCommand(command="start", description="Розпочати"),
        BotCommand(command="gpt", description="Чат бот"),
        BotCommand(command="random", description="Випадковий факт"),
        BotCommand(command="help", description="Справка"),
    ])


async def main():
    logging.basicConfig(level=logging.INFO,
                        # filename=settings.LOG_PATH,
                        stream=sys.stdout,
                        format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
                        filemode="w", encoding="utf-8"
                        )
    bot = Bot(settings.BOT_API_KEY)
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
