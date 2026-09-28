import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from utils.utils import image_path, load_message
from keyboards.reply import main_menu_kb
from keyboards import inline as inline_kb

router = Router(name = "common")

logger = logging.getLogger(__name__)


async def show_main_menu(message: Message, state: FSMContext):
    """Показує головне меню"""
    await state.clear()
    await message.answer_photo(
        photo=FSInputFile(image_path("main")),
        caption=load_message("main"),
        reply_markup=main_menu_kb,
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

@router.callback_query(F.data == inline_kb.CB_FINISH)
async def handle_finish(callback: CallbackQuery, state: FSMContext):
    """Кнопка закінчити яка завершує певну гілку"""
    logging.info(f"Користувач {callback.message.from_user.first_name}  завершив роботу в гілці")
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    await show_main_menu(callback.message, state)
