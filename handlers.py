import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

import keyboards.reply as reply_kb
import keyboards.inline as inline_kb
from utils.logger_config import setup_logging
from utils.utils import image_path, load_message

router = Router()

setup_logging()

async def show_main_menu(message: Message, state: FSMContext):
    """Показує головне меню"""
    await state.clear()
    await message.answer_photo(
        photo=FSInputFile(image_path("main")),
        caption=load_message("main"),
        reply_markup=reply_kb.main_menu_kb,
    )

@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext):
    logging.info(f"Користувач {message.from_user.first_name} натиснув /start")
    await show_main_menu(message, state)

@router.message(Command(commands=["help"]))
async def handle_help(message: Message):
    logging.info(f"Користувач {message.from_user.first_name} натиснув /help")
    await message.answer("Доступні команди:\n"
                         "/start - Розпочати\n"
                         "/gpt - Чат бот\n"
                         "/random - Випадковий факт\n"
                         "/help - Справка")

@router.message(F.text == reply_kb.BTN_GPT)
async def handle_gpt(message: Message):
    await message.answer("Заглушка на чат бот")

@router.message(F.text == reply_kb.BTN_FACT)
async def handle_fact(message: Message):
    await message.answer("Заглушка на чат цікавий факт")

@router.message(F.text == reply_kb.BTN_TALK)
async def handle_talk(message: Message):
    await message.answer("Обери особистість з якою ти би хотів поспілкуватись:")

@router.message(F.text == reply_kb.BTN_QUIZ)
async def handle_quiz(message: Message):
    await message.answer("Заглушка на чат quiz")
