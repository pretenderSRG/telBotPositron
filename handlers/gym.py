import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

import keyboards.inline as inline_kb
import keyboards.reply as reply_kb
from catalog import DAYS, EQUIPMENT, FALLBACK, GYM
from chat_gpt import ask
from utils.utils import load_prompt, image_path, load_message

logger = logging.getLogger(__name__)
router = Router(name="gym")


class GymStates(StatesGroup):
    program = State()
    days = State()
    equipment = State()


@router.message(Command("gym"))
@router.message(F.text == reply_kb.BTN_GYM)
async def handle_gym(message: Message, state: FSMContext):
    logger.info("Користувач %s вибрав команду /gym", message.from_user.username or message.from_user.username)
    await state.clear()
    await state.set_state(GymStates.program)
    await message.answer_photo(photo=FSInputFile(image_path("gym")),
                               caption=load_message("gym"),
                               reply_markup=inline_kb.finish_kb)
    await message.answer(
        "Обери тип програми тренувань:",
        reply_markup=inline_kb.gym_programs_kb(),
    )


@router.callback_query(inline_kb.GymCallback.filter())
async def handle_gym_choice(
    callback: CallbackQuery,
    callback_data: inline_kb.GymCallback,
    state: FSMContext,
):
    await callback.answer()

    current_state = await state.get_state()
    value = callback_data.value

    if (
        callback_data.step == "program"
        and current_state == GymStates.program.state
        and value in GYM
    ):
        await state.update_data(gym_program=value)
        await state.set_state(GymStates.days)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            f"Програма: <b>{GYM[value]}</b>\nКількість днів тренування в тиждень?",
            reply_markup=inline_kb.gym_days_kb(),
        )
        logger.info("Вибрана програма тренувань '%s'", value)
        return

    if (
        callback_data.step == "days"
        and current_state == GymStates.days.state
        and value in DAYS
    ):
        await state.update_data(days=value)
        await state.set_state(GymStates.equipment)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            f"Кількість днів тренування в тиждень: <b>{DAYS[value]}</b>\n"
            "Доступне обладнання:",
            reply_markup=inline_kb.gym_equipment_kb(),
        )
        logger.info("Вибрано %s днів тренувань", value)
        return

    if (
        callback_data.step == "equipment"
        and current_state == GymStates.equipment.state
        and value in EQUIPMENT
    ):
        await state.update_data(equipment=value)
        logger.info("Вибране обладнання - '%s'", value)
        data = await state.get_data()
        await callback.message.edit_text(
            f"Кількість днів тренування в тиждень: <b>{DAYS[data['days']]}</b>\n"
            f"Доступне обладнання: <b>{EQUIPMENT[value]}</b>",
            reply_markup=None,
        )
        await send_gym_program(callback.message, state)
        logger.info("Програму тренувань надіслано")
        return

    await callback.message.answer(
        "Цей вибір уже неактуальний. Почни заново: /gym"
    )
    logger.warning("Не актуальний вибір %s", value)


async def send_gym_program(message: Message, state: FSMContext) -> None:
    data: dict = await state.get_data()
    prompt = load_prompt("gym").format(
        gym_program=GYM[data["gym_program"]],
        days=DAYS[data["days"]],
        equipment=EQUIPMENT[data["equipment"]],
    )

    async with ChatActionSender.typing(
        bot=message.bot,
        chat_id=message.chat.id,
    ):
        response = await ask(system_prompt=prompt)

    await state.clear()

    if response is None:
        await message.answer(FALLBACK, reply_markup=inline_kb.finish_kb)
        return

    if isinstance(response, list):
        for index, part in enumerate(response):
            await message.answer(
                part,
                reply_markup=(
                    inline_kb.finish_kb
                    if index == len(response) - 1
                    else None
                ),
            )
        return

    await message.answer(response, reply_markup=inline_kb.finish_kb)
