from aiogram import Router

from bot.handlers import faq, menu, start, survey


def get_root_router() -> Router:
    router = Router(name="root")
    router.include_router(start.router)
    router.include_router(survey.router)
    router.include_router(faq.router)
    router.include_router(menu.router)
    return router
