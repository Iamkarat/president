# PRESIDENT — Telegram-бот

Премиальный Telegram-бот агентства PRESIDENT на aiogram 3.x.

## Структура проекта

```
bot/
    handlers/     — обработчики команд и сообщений
    keyboards/    — reply и inline клавиатуры
    services/     — статический контент, уведомления менеджеру
    database/     — подключение к БД и репозиторий
    models/       — модели SQLAlchemy
    states/       — состояния FSM
    utils/        — логирование
    config.py     — загрузка настроек из .env
    main.py        — точка входа
```

## Установка

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env`:

```
BOT_TOKEN=токен_бота
ADMIN_CHAT_ID=id_чата_менеджера
DATABASE_URL=sqlite+aiosqlite:///president.db
```

Для PostgreSQL используйте `DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname`.

## Запуск

```bash
python -m bot.main
```

## Запуск в Docker

```bash
docker compose up --build -d
```

или напрямую:

```bash
docker build -t president-bot .
docker run --env-file .env president-bot
```

## Команды бота

- `/start` — приветствие и главное меню
- `/menu` — открыть главное меню
- `/help` — справка по командам
- `/cancel` — отменить текущее действие (например, заполнение анкеты)
