"Модуль для работы с запросами в бд"

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import Note


async def insert_obj(
    async_session: async_sessionmaker[AsyncSession],
    obj: Note,
) -> None:
    "Функция создаёт объект в бд"
    async with async_session() as session:
        async with session.begin():
            session.add(instance=obj)
            await session.commit()


async def select_many(
    async_session: async_sessionmaker[AsyncSession],
    owner_id: int
) -> Sequence[Note]:
    "Функция возвращает множество объектов"
    async with async_session() as session:
        stmt = select(Note).filter(Note.owner_id == owner_id).order_by(Note.created)
        result = await session.execute(stmt)
        return result.scalars().all()


async def select_one(
    async_session: async_sessionmaker[AsyncSession],
    note_id: int
) -> Note | None:
    "Функция возвращает один объект"
    async with async_session() as session:
        stmt = select(Note).filter(Note.id == note_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def delete(
    async_session: async_sessionmaker[AsyncSession],
    note_id: int
) -> None:
    "Функция удаляет объект по id"
    async with async_session() as session:
        async with session.begin():
            stmt = select(Note).filter(Note.id == note_id)
            result = await session.execute(stmt)
            note = result.scalar_one_or_none()

            if note is None:
                return None

            await session.delete(note)
            await session.commit()
