"Модуль подключения к базе данных"

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    url="sqlite+aiosqlite:///sqlite3.db",
    echo=True
)

session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
