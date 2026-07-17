from aiogram import F, Router
from aiogram.types import Message

from bot.keyboards.inline import back_to_menu_keyboard
from bot.services.content import (
    ARTICLES,
    FIRST_STEPS_TEXT,
    LIFESTYLE_TEXT,
    LUXURY_TEXT,
    NEWS_TEXT,
    SECURITY_TEXT,
    STORIES,
    WORK_TEXT,
)

router = Router(name="menu")


@router.message(F.text == "📖 Истории девушек")
async def show_stories(message: Message) -> None:
    for story in STORIES[:-1]:
        await message.answer(story)
    await message.answer(STORIES[-1], reply_markup=back_to_menu_keyboard())


@router.message(F.text == "🚀 Первые шаги")
async def show_first_steps(message: Message) -> None:
    await message.answer(FIRST_STEPS_TEXT, reply_markup=back_to_menu_keyboard())


@router.message(F.text == "🏙 Lifestyle")
async def show_lifestyle(message: Message) -> None:
    await message.answer(LIFESTYLE_TEXT, reply_markup=back_to_menu_keyboard())


@router.message(F.text == "💼 Работа")
async def show_work(message: Message) -> None:
    await message.answer(WORK_TEXT, reply_markup=back_to_menu_keyboard())


@router.message(F.text == "🛡 Безопасность")
async def show_security(message: Message) -> None:
    await message.answer(SECURITY_TEXT, reply_markup=back_to_menu_keyboard())


@router.message(F.text == "📚 Разборы")
async def show_articles(message: Message) -> None:
    for article in ARTICLES[:-1]:
        await message.answer(article)
    await message.answer(ARTICLES[-1], reply_markup=back_to_menu_keyboard())


@router.message(F.text == "📰 Новости")
async def show_news(message: Message) -> None:
    await message.answer(NEWS_TEXT, reply_markup=back_to_menu_keyboard())


@router.message(F.text == "💎 Luxury Life")
async def show_luxury(message: Message) -> None:
    await message.answer(LUXURY_TEXT, reply_markup=back_to_menu_keyboard())
