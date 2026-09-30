from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

BTN_GPT = "🤖 Чат-бот"
BTN_FACT = "🧠 Цікавий факт"
BTN_TALK = "👤 Відома особистість"
BTN_QUIZ = "❓ Квіз"
BTN_TRANSLATE = "🏋️‍♀️ Тренування"
BTN_RECOMMEND = "🍿 Що подивитись"

MENU_BUTTONS = {BTN_QUIZ, BTN_TALK, BTN_FACT, BTN_GPT, BTN_TRANSLATE, BTN_RECOMMEND}


main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_GPT), KeyboardButton(text=BTN_FACT)],
        [KeyboardButton(text=BTN_TALK), KeyboardButton(text=BTN_QUIZ)],
        [KeyboardButton(text=BTN_TRANSLATE), KeyboardButton(text=BTN_RECOMMEND)]
    ],
    resize_keyboard=True,
    input_field_placeholder="Обери пункт меню",
)