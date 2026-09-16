import asyncio

from aiogram import Bot,Dispatcher
from aiogram.types import Message

from config import settings
from handlers import router


async def main():
    bot = Bot(settings.BOT_API_KEY)
    dp = Dispatcher()

    dp.include_routers(router,)

    print("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Зупинка бота...")
