from aiogram import Router, F
from aiogram.types import Message

import keyboards.reply as reply_kb


router = Router(name = "celebrity_talk")


@router.message(F.text == reply_kb.BTN_TALK)
async def handle_talk(message: Message):
    await message.answer("Обери особистість з якою ти би хотів поспілкуватись:")