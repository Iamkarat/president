import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str
    admin_chat_id: int
    database_url: str
    log_level: str


def load_config() -> Config:
    return Config(
        bot_token=os.getenv("BOT_TOKEN", ""),
        admin_chat_id=int(os.getenv("ADMIN_CHAT_ID", "0")),
        database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///president.db"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


config = load_config()
