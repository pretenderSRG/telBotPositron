import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile

import keyboards.inline as inline_kb
import keyboards.reply as reply_kb
from catalog import FALLBACK
from chat_gpt import ask
from filters import USER_TEXT
from utils.utils import load_message, load_prompt, image_path

router = Router(name="gpt")
logger = logging.getLogger(__name__)


class GPTStates(StatesGroup):
    dialog = State()


async def start_gpt_dialog(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.first_name} увійшов у режим GPT")
    await state.clear()
    await state.set_state(GPTStates.dialog)

    await message.answer_photo(photo=FSInputFile(image_path("gpt")),
                               caption=load_message("gpt"),
                               reply_markup=inline_kb.finish_kb)

@router.message(F.text == reply_kb.BTN_GPT)
@router.message(Command("gpt"))
async def handle_command_gpt(message: Message, state: FSMContext):
    await start_gpt_dialog(message, state)


@router.message(GPTStates.dialog, USER_TEXT)
async def handle_gpt_message(message: Message):
    text = await ask(load_prompt("gpt"), message.text)

    if text is None:
        await message.answer(FALLBACK)
        return

    if isinstance(text, list):
        for ind, text_item in enumerate(text):
            await message.answer(
                text_item,
                reply_markup=(
                    inline_kb.finish_kb if ind == len(text) - 1 else None
                ),
            )
        return

    await message.answer(text, reply_markup=inline_kb.finish_kb)
