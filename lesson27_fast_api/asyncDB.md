# Код для асинхронної роботи з базою даних:

```python
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from app.models import Item, ItemCreate, ItemUpdate


async def create_item(session: AsyncSession, item_data: ItemCreate) -> Item:
    item = Item.from_orm(item_data)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def get_item(session: AsyncSession, item_id: int) -> Optional[Item]:
    return await session.get(Item, item_id)


async def get_items(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Item]:
    statement = select(Item).offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_item(session: AsyncSession, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
    item = await session.get(Item, item_id)
    if not item:
        return None
    item_data_dict = item_data.dict(exclude_unset=True)
    for key, value in item_data_dict.items():
        setattr(item, key, value)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(session: AsyncSession, item_id: int) -> bool:
    item = await session.get(Item, item_id)
    if not item:
        return False
    await session.delete(item)
    await session.commit()
    return True
```

# **Основні зміни:**

1. **AsyncSession замість Session** - використовується `AsyncSession` з `sqlmodel.ext.asyncio.session`
2. **async/await** - всі функції тепер асинхронні (`async def`) і операції з БД виконуються через `await`
3. **Асинхронні операції:**
   - `await session.commit()` - асинхронний коміт
   - `await session.refresh()` - асинхронне оновлення об'єкта
   - `await session.get()` - асинхронне отримання об'єкта
   - `await session.exec()` - асинхронне виконання запиту

**Додатково знадобиться:**
- Асинхронний драйвер БД (наприклад, `asyncpg` для PostgreSQL або `aiomysql` для MySQL)
- Налаштування асинхронного engine при створенні з'єднання з БД

# Ось налаштування асинхронного engine для SQLite:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# URL для асинхронного SQLite (використовує aiosqlite)
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Створення асинхронного engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логування SQL-запитів (можна вимкнути в production)
    future=True,
    connect_args={"check_same_thread": False}  # Для SQLite
)

# Створення фабрики сесій
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


# Функція для створення таблиць
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Dependency для отримання сесії в FastAPI
async def get_session():
    async with async_session() as session:
        yield session
```

**Встановіть необхідні пакети:**

```bash
pip install aiosqlite sqlalchemy[asyncio]
```

**Використання в FastAPI:**

```python
from fastapi import FastAPI, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

app = FastAPI()

# Створення таблиць при старті
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

# Приклад ендпоінту
@app.get("/items/{item_id}")
async def read_item(
    item_id: int,
    session: AsyncSession = Depends(get_session)
):
    item = await get_item(session, item_id)
    return item
```

**Важливі моменти:**
- Використовується `sqlite+aiosqlite://` замість `sqlite://`
- `expire_on_commit=False` запобігає проблемам з доступом до атрибутів після коміту
- `check_same_thread=False` необхідний для SQLite в асинхронному режимі