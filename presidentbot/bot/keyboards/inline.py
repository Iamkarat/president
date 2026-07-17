from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.services.content import FAQ_ITEMS


def welcome_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🤝 Познакомиться с PRESIDENT", callback_data="welcome_start")
    return builder.as_markup()


def faq_list_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for index, (question, _) in enumerate(FAQ_ITEMS):
        builder.button(text=question, callback_data=f"faq:{index}")
    builder.adjust(1)
    return builder.as_markup()


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Вернуться в меню", callback_data="back_to_menu")
    return builder.as_markup()


def faq_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Ко всем вопросам", callback_data="faq_back")
    return builder.as_markup()


def yes_no_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да", callback_data="experience:yes")
    builder.button(text="❌ Нет", callback_data="experience:no")
    return builder.as_markup()


def photos_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📸 Да", callback_data="has_photos:professional")
    builder.button(text="📷 Только обычные", callback_data="has_photos:casual")
    builder.button(text="❌ Пока нет", callback_data="has_photos:none")
    builder.adjust(1)
    return builder.as_markup()


def continue_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➡ Продолжить", callback_data="photos_continue")
    return builder.as_markup()


def skip_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏭ Пропустить", callback_data="skip_social")
    return builder.as_markup()
