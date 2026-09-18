import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import keyboards as kb

router = Router()

@router.message(CommandStart())
async def handle_start(message: Message):
    logging.info(f"Користувач {message.from_user.first_name} натиснув /start")
    await message.answer(text=f"Привіт {message.from_user.first_name}!",
                         reply_markup = kb.main_menu_kb)

@router.message(Command(commands=["help"]))
async def handle_help(message: Message):
    logging.info(f"Користувач {message.from_user.first_name} натиснув /help")
    await message.answer("Доступні команди:\n"
                         "/start - Розпочати\n"
                         "/gpt - Чат бот\n"
                         "/random - Випадковий факт\n"
                         "/help - Справка")

@router.message(F.text == kb.BTN_CHATBOT)
async def handle_chatbot(message: Message):
    await message.answer("Заглушка на чат бот")

@router.message(F.text == kb.BTN_FACT)
async def handle_fact(message: Message):
    await message.answer("Заглушка на чат цікавий факт")

@router.message(F.text == kb.BTN_FAMOUS_PERSON)
async def handle_famous_person(message: Message):
    await message.answer("Обери особистість з якою ти би хотів поспілкуватись:", reply_markup=kb.famous_people_inline_kb)

@router.message(F.text == kb.BTN_SETTINGS)
async def handle_settings(message: Message):
    await message.answer("Заглушка на чат налаштування")


@router.message(F.sticker)
async def handle_sticker(message: Message):
    await message.answer("Це стікер")

@router.message(F.photo)
async def handle_photo(message: Message):
    await message.answer("Це фото")

@router.callback_query(F.data.startswith("famous_person_"))
async def handle_famous_person(callback: CallbackQuery):
    await callback.message.answer(f"Ти натиснув - {kb.famous_people[callback.data]}")
    await callback.answer()