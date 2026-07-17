import logging
import sys

from bot.config import config


def setup_logging() -> None:
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("bot.log", encoding="utf-8"),
        ],
    )
    logging.getLogger("aiogram").setLevel(logging.WARNING)
