from aiogram import Router, F
from aiogram.types import Message
import keyboards.reply as reply
from chat_gpt import ask
from utils.utils import load_prompt

router = Router(name = "random_fact")

@router.message(F.text == reply.BTN_FACT)
async def handle_fact(message: Message):
    text = await ask(load_prompt("random"), message.text)
    await message.answer("Заглушка на чат цікавий факт")