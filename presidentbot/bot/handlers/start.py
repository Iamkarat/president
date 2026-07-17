import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import welcome_keyboard
from bot.keyboards.reply import main_menu
from bot.services.content import MENU_INTRO_TEXT, WELCOME_TEXT

logger = logging.getLogger(__name__)
router = Router(name="start")

HELP_TEXT = (
    "ℹ️ <b>Помощь</b>\n\n"
    "/start — начать работу с ботом\n"
    "/menu — открыть главное меню\n"
    "/cancel — отменить текущее действие (например, заполнение анкеты)\n"
    "/help — показать это сообщение"
)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    logger.info("Пользователь %s запустил бота", message.from_user.id)
    await message.answer(WELCOME_TEXT, reply_markup=welcome_keyboard())


@router.callback_query(F.data == "welcome_start")
async def on_welcome_start(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer(MENU_INTRO_TEXT, reply_markup=main_menu())
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def on_back_to_menu(callback: CallbackQuery) -> None:
    await callback.message.answer(MENU_INTRO_TEXT, reply_markup=main_menu())
    await callback.answer()


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(MENU_INTRO_TEXT, reply_markup=main_menu())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Сейчас нечего отменять.", reply_markup=main_menu())
        return
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=main_menu())
