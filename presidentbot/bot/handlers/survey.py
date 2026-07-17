import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.repository import save_survey
from bot.keyboards.inline import (
    continue_keyboard,
    photos_type_keyboard,
    skip_keyboard,
    yes_no_keyboard,
)
from bot.keyboards.reply import main_menu
from bot.services.notify import notify_admin_new_survey
from bot.states.survey import SurveyForm

logger = logging.getLogger(__name__)
router = Router(name="survey")

MIN_PHOTOS = 2
MAX_PHOTOS = 5


@router.message(F.text == "📝 Анкета модели")
async def start_survey(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(SurveyForm.name)
    await message.answer(
        "Спасибо за интерес к агентству <b>PRESIDENT</b> 💙\n\n"
        "Пожалуйста, ответьте на несколько вопросов.\n\n"
        "<b>Вопрос 1</b>\nКак вас зовут?"
    )


@router.message(SurveyForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Пожалуйста, введите ваше имя текстом.")
        return
    await state.update_data(name=message.text.strip())
    await state.set_state(SurveyForm.age)
    await message.answer("<b>Вопрос 2</b>\nСколько вам лет?")


@router.message(SurveyForm.age)
async def process_age(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.isdigit() or not (16 <= int(message.text) <= 60):
        await message.answer("Пожалуйста, укажите возраст числом, например: 21")
        return
    await state.update_data(age=int(message.text))
    await state.set_state(SurveyForm.city)
    await message.answer("<b>Вопрос 3</b>\nВ каком городе вы проживаете?")


@router.message(SurveyForm.city)
async def process_city(message: Message, state: FSMContext) -> None:
    if not message.text or len(message.text.strip()) < 2:
        await message.answer("Пожалуйста, укажите город текстом.")
        return
    await state.update_data(city=message.text.strip())
    await state.set_state(SurveyForm.height)
    await message.answer("<b>Вопрос 4</b>\nКакой у вас рост?\n\nНапример: 172 см")


@router.message(SurveyForm.height)
async def process_height(message: Message, state: FSMContext) -> None:
    if not message.text or not any(char.isdigit() for char in message.text):
        await message.answer("Пожалуйста, укажите рост числом, например: 172 см")
        return
    await state.update_data(height=message.text.strip())
    await state.set_state(SurveyForm.experience)
    await message.answer(
        "<b>Вопрос 5</b>\nЕсть ли опыт работы моделью?",
        reply_markup=yes_no_keyboard(),
    )


@router.callback_query(SurveyForm.experience, F.data.startswith("experience:"))
async def process_experience(callback: CallbackQuery, state: FSMContext) -> None:
    experience = callback.data.split(":")[1]
    await state.update_data(experience=experience)
    await state.set_state(SurveyForm.has_photos)
    await callback.message.edit_text(
        "<b>Вопрос 6</b>\nЕсть ли профессиональные фотографии?",
        reply_markup=photos_type_keyboard(),
    )
    await callback.answer()


@router.callback_query(SurveyForm.has_photos, F.data.startswith("has_photos:"))
async def process_has_photos(callback: CallbackQuery, state: FSMContext) -> None:
    has_photos = callback.data.split(":")[1]
    await state.update_data(has_photos=has_photos, photos=[])
    await state.set_state(SurveyForm.photos)
    await callback.message.edit_text(
        "<b>Вопрос 7</b>\nПрикрепите от 2 до 5 фотографий.\n\n"
        "Можно отправить альбомом или по одной."
    )
    await callback.answer()


@router.message(SurveyForm.photos, F.photo)
async def process_photos(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photos: list[str] = data.get("photos", [])

    if len(photos) >= MAX_PHOTOS:
        return

    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)

    if len(photos) >= MAX_PHOTOS:
        await state.set_state(SurveyForm.social)
        await message.answer(
            "Фотографии получены ✅\n\n"
            "<b>Вопрос 8</b>\nInstagram или Telegram (необязательно).",
            reply_markup=skip_keyboard(),
        )
    elif len(photos) >= MIN_PHOTOS:
        await message.answer(
            f"Получено фотографий: {len(photos)}. Можно добавить ещё или продолжить.",
            reply_markup=continue_keyboard(),
        )


@router.message(SurveyForm.photos)
async def process_photos_invalid(message: Message) -> None:
    await message.answer("Пожалуйста, отправьте фотографии (от 2 до 5 штук).")


@router.callback_query(SurveyForm.photos, F.data == "photos_continue")
async def process_photos_continue(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    photos: list[str] = data.get("photos", [])
    if len(photos) < MIN_PHOTOS:
        await callback.answer("Нужно как минимум 2 фотографии.", show_alert=True)
        return
    await state.set_state(SurveyForm.social)
    await callback.message.answer(
        "<b>Вопрос 8</b>\nInstagram или Telegram (необязательно).",
        reply_markup=skip_keyboard(),
    )
    await callback.answer()


@router.callback_query(SurveyForm.social, F.data == "skip_social")
async def process_social_skip(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(social=None)
    await state.set_state(SurveyForm.motivation)
    await callback.message.answer(
        "<b>Вопрос 9</b>\nПочему вы хотите стать моделью в PRESIDENT?"
    )
    await callback.answer()


@router.message(SurveyForm.social)
async def process_social(message: Message, state: FSMContext) -> None:
    await state.update_data(social=message.text.strip() if message.text else None)
    await state.set_state(SurveyForm.motivation)
    await message.answer("<b>Вопрос 9</b>\nПочему вы хотите стать моделью в PRESIDENT?")


@router.message(SurveyForm.motivation)
async def process_motivation(message: Message, state: FSMContext) -> None:
    if not message.text or len(message.text.strip()) < 3:
        await message.answer("Пожалуйста, ответьте текстом.")
        return

    await state.update_data(motivation=message.text.strip())
    data = await state.get_data()

    created_at = datetime.utcnow()
    await save_survey(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=data["name"],
        age=data["age"],
        city=data["city"],
        height=data["height"],
        experience=data["experience"],
        has_photos=data["has_photos"],
        photo_ids=",".join(data.get("photos", [])),
        social=data.get("social"),
        motivation=data["motivation"],
        created_at=created_at,
    )

    await notify_admin_new_survey(
        bot=message.bot,
        user=message.from_user,
        data=data,
        created_at=created_at.strftime("%d.%m.%Y %H:%M"),
    )
    logger.info("Новая анкета от пользователя %s сохранена", message.from_user.id)

    await state.clear()
    await message.answer(
        "✅ <b>Спасибо!</b>\n\n"
        "Ваша анкета успешно отправлена менеджеру.\n"
        "Мы внимательно её рассмотрим и свяжемся с вами в ближайшее время.",
        reply_markup=main_menu(),
    )
