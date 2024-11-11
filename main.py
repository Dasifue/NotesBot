"Основной выполняемый модуль"

import asyncio

from database import Base, engine

async def main() -> None:
    "Функция создаёт таблицы в бд и запускает проект"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(main())

