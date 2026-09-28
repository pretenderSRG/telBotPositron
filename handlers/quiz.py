import logging
import re

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

import keyboards.inline as inline_kb
import keyboards.reply as reply_kb
from catalog import FALLBACK, QUIZ_TOPICS
from chat_gpt import ask
from utils.utils import image_path, load_message, load_prompt

router = Router(name="quiz")
logger = logging.getLogger(__name__)

MAX_ASKED = 10
VERDICT_RE = re.compile(r"^\W*(НЕПРАВИЛЬНО|ПРАВИЛЬНО)\W*", re.IGNORECASE)


class QuizStates(StatesGroup):
    choosing_topic = State()
    answering_topic = State()
    waiting_next = State()


async def get_quiz_summary(state: FSMContext) -> str:
    current_state = await state.get_state()

    if current_state is None or current_state.startswith(QuizStates.__name__):
        return None

    data = await state.get_data()
    total = data.get("total", 0)

    if not total:
        return None
    return f"🏆 Твій результат: <b>{data.get('score', 0)} з {total}</b>"


def parse_verdict(text: str) -> tuple[bool | None, str]:
    """Розбирає відповіді. Якщо None — формат порушено."""
    match = VERDICT_RE.match(text)

    if match is None:
        return None, text

    is_correct = match.group(1).upper() == "ПРАВИЛЬНО"
    explanation = text[match.end():].strip()

    return is_correct, explanation


async def send_question(message: Message, state: FSMContext):
    """Питає у моделі нове питання за обраною темою."""
    data = await state.get_data()
    topic = data["topic"]
    asked = data.get("asked", [])

    prompt = load_prompt("quiz_question").format(
        topic=QUIZ_TOPICS[topic],
        asked="\n".join(f"- {q}" for q in asked) or "(ще не було)",
    )

    async with ChatActionSender.typing(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        question = await ask(prompt)

        if question is None:
            await state.set_state(QuizStates.waiting_next)
            await message.answer(
                FALLBACK,
                reply_markup=inline_kb.quiz_result_kb,
            )
            return

    first_line = question.splitlines()[0]
    await state.update_data(question=question, asked=[*asked, first_line][-MAX_ASKED:],)
    await state.set_state(QuizStates.answering_topic)

    await message.answer(
        f"{question}\n\n✍Напиши відповідь — букву або текст варіанта.",
        reply_markup=inline_kb.finish_kb,
    )


@router.message(Command("quiz"))
@router.message(F.text == reply_kb.BTN_QUIZ)
async def handle_quiz(message: Message, state: FSMContext):
    logger.info("Користувач %s почав квіз", message.from_user.id)

    await state.clear()
    await state.set_state(QuizStates.choosing_topic)
    await state.set_data({"score": 0, "total": 0})

    await message.answer_photo(
        photo=FSInputFile(image_path("quiz")),
        caption=load_message("quiz"),
        reply_markup=inline_kb.quiz_topics_kb(),
    )


@router.callback_query(inline_kb.QuizTopicCallback.filter())
async def handle_chose_topic(
    callback: CallbackQuery,
    callback_data: inline_kb.QuizTopicCallback,
    state: FSMContext,
):
    await callback.answer()
    await state.update_data(topic=callback_data.topic)
    await send_question(callback.message, state)

