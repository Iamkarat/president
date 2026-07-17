from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Survey(Base):
    __tablename__ = "surveys"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(255))
    height: Mapped[str] = mapped_column(String(50))
    experience: Mapped[str] = mapped_column(String(20))
    has_photos: Mapped[str] = mapped_column(String(50))
    photo_ids: Mapped[str] = mapped_column(Text)
    social: Mapped[str | None] = mapped_column(String(255), nullable=True)
    motivation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
