from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BTN_GPT = "Чат-бот"
BTN_FACT = "Цікавий факт"
BTN_TALK = "Відома особистість"
BTN_QUIZ = "Налаштування"


main_menu_kb = ReplyKeyboardMarkup(keyboard=
[
    [
        KeyboardButton(text=BTN_GPT),
        KeyboardButton(text=BTN_FACT),
        KeyboardButton(text=BTN_TALK),
        KeyboardButton(text=BTN_QUIZ),
    ]
],
    resize_keyboard=True,
    input_field_placeholder="Обери пункт меню"
)