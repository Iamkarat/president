import logging

from aiogram import Bot
from aiogram.types import InputMediaPhoto, User

from bot.config import config

logger = logging.getLogger(__name__)

EXPERIENCE_LABELS = {"yes": "Есть", "no": "Нет"}
PHOTOS_LABELS = {
    "professional": "Есть профессиональные",
    "casual": "Только обычные",
    "none": "Пока нет",
}


async def notify_admin_new_survey(
    bot: Bot,
    user: User,
    data: dict,
    created_at: str,
) -> None:
    caption = (
        "📝 <b>Новая анкета модели</b>\n\n"
        f"👤 Имя: {data['name']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"🏙 Город: {data['city']}\n"
        f"📏 Рост: {data['height']}\n"
        f"💼 Опыт: {EXPERIENCE_LABELS.get(data['experience'], data['experience'])}\n"
        f"📸 Фото: {PHOTOS_LABELS.get(data['has_photos'], data['has_photos'])}\n"
        f"🔗 Instagram/Telegram: {data.get('social') or 'не указано'}\n\n"
        f"💬 Почему хочет стать моделью:\n{data['motivation']}\n\n"
        f"🆔 ID пользователя: {user.id}\n"
        f"👤 Username: @{user.username if user.username else 'отсутствует'}\n"
        f"📅 Дата заполнения: {created_at}"
    )

    photo_ids: list[str] = data.get("photos", [])
    try:
        if photo_ids:
            media = [InputMediaPhoto(media=photo_ids[0], caption=caption, parse_mode="HTML")]
            media += [InputMediaPhoto(media=pid) for pid in photo_ids[1:10]]
            await bot.send_media_group(chat_id=config.admin_chat_id, media=media)
        else:
            await bot.send_message(chat_id=config.admin_chat_id, text=caption)
        logger.info("Анкета пользователя %s отправлена менеджеру", user.id)
    except Exception:
        logger.exception("Не удалось отправить анкету пользователя %s менеджеру", user.id)
