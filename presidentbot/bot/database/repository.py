from bot.database.engine import async_session, engine
from bot.models.survey import Base, Survey


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_survey(**fields) -> Survey:
    async with async_session() as session:
        survey = Survey(**fields)
        session.add(survey)
        await session.commit()
        await session.refresh(survey)
        return survey
