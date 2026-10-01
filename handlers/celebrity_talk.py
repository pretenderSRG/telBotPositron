import html
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

import keyboards.inline as inline_kb
import keyboards.reply as reply_kb
from catalog import FALLBACK
from config import settings
from filters import USER_TEXT
from chat_gpt import ask_history, check_person_exists
from utils.utils import load_prompt, image_path, load_message

logger = logging.getLogger(__name__)
router = Router(name="person_talk")


class TalkStates(StatesGroup):
    choosing = State()
    dialog = State()


@router.message(Command("talk"))
@router.message(F.text == reply_kb.BTN_TALK)
async def handle_talk(message: Message, state: FSMContext):
    logger.info("Користувач %s розпочав діалог з персонажем", message.from_user.username or message.from_user.first_name)
    await state.clear()
    await state.set_state(TalkStates.choosing)
    await message.answer_photo(photo=FSInputFile(image_path("talk")),
                               caption=load_message("talk"),
                               reply_markup=inline_kb.finish_kb)
    await message.answer(
        "Введи ім'я персонажа, з яким хочеш поспілкуватися:"
    )


@router.message(TalkStates.choosing, USER_TEXT)
async def handle_choose_person(message: Message, state: FSMContext):
    person = message.text.strip()
    if not person or len(person) > 20:
        await message.answer("Введи ім'я довжиною до 20 символів.")
        return

    async with ChatActionSender.typing(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        exists = await check_person_exists(person)

    if exists is None:
        await message.answer(FALLBACK)
        return
    if not exists:
        await message.answer(
            "Не вдалося знайти такого персонажа. Спробуй інше ім'я."
        )
        logger.warning("Персонажа %s не існує", person)
        return

    await state.set_data({
        "person": person,
        "history": [],
    })
    await state.set_state(TalkStates.dialog)

    logger.info("Користувач %s говорить з %s", message.from_user.username or message.from_user.first_name, person)
    await message.answer(
        text=(
            f"Ти говориш з <b>{html.escape(person)}</b>. "
            "Напиши перше повідомлення 👇"
        ),
        reply_markup=inline_kb.finish_kb
    )


@router.message(TalkStates.dialog, USER_TEXT)
async def handle_talk_message(message: Message, state: FSMContext):
    data = await state.get_data()
    person = data["person"]
    history = [*data["history"], {"role": "user", "content": message.text}]

    async with ChatActionSender.typing(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        text = await ask_history(
            system_prompt=load_prompt("person").format(person=person),
            history=history
        )

    if text is None:
        await message.answer(FALLBACK, reply_markup=inline_kb.finish_kb)
        return

    response = "\n".join(text) if isinstance(text, list) else text
    history.append({"role": "assistant", "content": response})
    await state.update_data(history=history[-settings.MAX_GPT_HISTORY:])

    parts = text if isinstance(text, list) else [text]
    for i, part in enumerate(parts):
        await message.answer(
            text=part,
            reply_markup=(
                inline_kb.finish_kb if i == len(parts) - 1 else None
            ),
        )
