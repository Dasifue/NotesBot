"Основной выполняемый модуль"

import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from database import Base, engine

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "bot token")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main() -> None:
    "Функция создаёт таблицы в бд и запускает проект"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
