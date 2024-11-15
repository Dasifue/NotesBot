"Основной выполняемый модуль"

import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from database import Base, Note, session, engine, utils

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "bot token")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main() -> None:
    "Функция создаёт таблицы в бд и запускает проект"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    note = Note(
        owner_id = 1,
        title = "Test",
        content = "Some content"
    )
    await utils.insert_obj(session, note)

if __name__ == "__main__":
    asyncio.run(main())
