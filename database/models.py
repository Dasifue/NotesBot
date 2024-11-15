"Модуль для работы с ORM моделями"

import datetime

from sqlalchemy import func, types
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(AsyncAttrs, DeclarativeBase):
    "Родительский мета класс для моделей бд"


class Note(Base):
    "модель таблицы 'Запись'"
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(types.String(100), nullable=False)
    content: Mapped[str] = mapped_column(types.Text())
    created: Mapped[datetime.datetime] = mapped_column(server_default=func.now()) # type: ignore

    def __repr__(self):
        return f"Note: {self.title}"
