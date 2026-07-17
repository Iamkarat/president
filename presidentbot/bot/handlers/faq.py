from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import faq_back_keyboard, faq_list_keyboard
from bot.services.content import FAQ_ITEMS

router = Router(name="faq")


@router.message(F.text == "❓ FAQ")
async def show_faq_list(message: Message) -> None:
    await message.answer(
        "❓ <b>Часто задаваемые вопросы</b>\n\nВыберите вопрос, чтобы увидеть ответ:",
        reply_markup=faq_list_keyboard(),
    )


@router.callback_query(F.data.startswith("faq:"))
async def show_faq_answer(callback: CallbackQuery) -> None:
    index = int(callback.data.split(":")[1])
    question, answer = FAQ_ITEMS[index]
    await callback.message.edit_text(
        f"❓ <b>{question}</b>\n\n{answer}",
        reply_markup=faq_back_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "faq_back")
async def back_to_faq_list(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "❓ <b>Часто задаваемые вопросы</b>\n\nВыберите вопрос, чтобы увидеть ответ:",
        reply_markup=faq_list_keyboard(),
    )
    await callback.answer()
