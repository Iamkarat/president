from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MENU_BUTTONS = [
    ["📖 Истории девушек", "🚀 Первые шаги"],
    ["🏙 Lifestyle", "💼 Работа"],
    ["🛡 Безопасность", "📚 Разборы"],
    ["📰 Новости", "💎 Luxury Life"],
    ["❓ FAQ", "📝 Анкета модели"],
]


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn) for btn in row] for row in MENU_BUTTONS],
        resize_keyboard=True,
    )
