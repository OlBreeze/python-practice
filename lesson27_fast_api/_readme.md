# Конспект лекции: FastAPI - асинхронный веб-фреймворк Python

## 1. Введение в FastAPI

### 1.1 Что такое FastAPI?
FastAPI — это современный, высокопроизводительный веб-фреймворк для создания API на Python, основанный на стандартных аннотациях типов Python. Версия фреймворка на ноябрь 2025 года — **0.122.0**.

### 1.2 Ключевые особенности
- **Скорость**: По производительности сравним с Node.js и Go благодаря использованию Starlette и Pydantic
- **Асинхронность**: Изначально разработан как полностью асинхронный фреймворк (в отличие от Django и Flask)
- **Автоматическая документация**: Генерация интерактивной документации через Swagger UI и ReDoc
- **Валидация данных**: Автоматическая проверка данных через Pydantic
- **Аннотации типов**: Полная поддержка type hints Python 3.8+

### 1.3 Сравнение с Django
| Django | FastAPI |
|--------|---------|
| Синхронный (по умолчанию) | Асинхронный |
| Жесткая структура проекта | Гибкая структура |
| Автоматическая генерация файлов | Ручное создание файлов |
| Встроенная админ-панель, ORM | Минималистичный подход |
| WSGI | ASGI (Asynchronous Server Gateway Interface) |

---

## 2. Выбор хостинга для деплоя

### 2.1 Критерии выбора хостинга
1. **Ресурсоемкость проекта** - сколько ресурсов потребляет приложение
2. **Характеристики и цена** - что предлагает хостинг за какую цену
3. **Количество пользователей** - ожидаемая нагрузка
4. **Uptime серверов** - надежность хостинг-провайдера
5. **Предустановленное ПО** - ОС, веб-серверы (например, Nginx)
6. **Веб-панель управления** - удобство работы с файлами
7. **HTTPS-сертификаты** - автоматическое подписание SSL
8. **Защита** - аутентификация, доступ к консоли
9. **Консольный доступ** - возможность клонировать репозиторий, устанавливать зависимости
10. **Static files** - сбор и раздача статических файлов
11. **Мониторинг** - инструменты отслеживания трафика

### 2.2 Типы серверов
- **VPS (Virtual Private Server)** - виртуальный контейнер на общем сервере
- **VDS (Virtual Dedicated Server)** - выделенная машина с большими возможностями, можно разворачивать несколько проектов

---

## 3. Установка и настройка проекта

### 3.1 Установка зависимостей
```bash
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlmodel
```

Или с полным набором:
```bash
pip install "fastapi[standard]"
```

### 3.2 Основные зависимости
- **FastAPI** - сам фреймворк
- **Uvicorn** - ASGI-сервер для запуска приложения
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация данных
- **Starlette** - базовый веб-фреймворк (под капотом FastAPI)
- **SQLModel** - упрощенная работа с моделями

### 3.3 Запуск сервера
```bash
# Стандартный запуск (порт 8000)
uvicorn main:app --reload

# На кастомном порту
uvicorn main:app --reload --port 8002
```

---

## 4. Структура проекта FastAPI

### 4.1 Базовая структура
```
project/
├── app/
│   ├── __init__.py          # Пакет приложения
│   ├── main.py              # Точка входа
│   ├── models.py            # Pydantic модели (схемы)
│   ├── database.py          # Настройка БД
│   ├── crud.py              # CRUD операции
│   └── routers/
│       ├── __init__.py
│       └── items.py         # Маршруты
├── requirements.txt
└── alembic/                 # Миграции (опционально)
```

### 4.2 Файл main.py (точка входа)
```python
from fastapi import FastAPI
from app.routers import items

app = FastAPI(
    title="My API",
    description="API Description",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Hello Fast API"}
```

### 4.3 Файл models.py (Pydantic схемы)
```python
from typing import Optional
from pydantic import BaseModel, Field

# Схема для создания
class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float

# Схема для чтения
class ItemRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool = True

# Схема для обновления
class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
```

### 4.4 Файл database.py (настройка БД)
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL базы данных
DATABASE_URL = "sqlite:///./app.db"

# Создание engine
engine = create_engine(DATABASE_URL, echo=True)

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Инициализация БД
def init_db():
    Base.metadata.create_all(bind=engine)
```

### 4.5 Файл crud.py (операции с БД)
```python
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Item, ItemCreate, ItemUpdate

# CREATE
def create_item(session: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# READ (список)
def get_items(session: Session, skip: int = 0, limit: int = 10):
    statement = select(Item).offset(skip).limit(limit)
    result = session.execute(statement)
    return result.scalars().all()

# READ (один элемент)
def get_item(session: Session, item_id: int):
    return session.get(Item, item_id)

# UPDATE
def update_item(session: Session, item_id: int, item_update: ItemUpdate):
    db_item = session.get(Item, item_id)
    if not db_item:
        return None
    
    item_data = item_update.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

# DELETE
def delete_item(session: Session, item_id: int):
    db_item = session.get(Item, item_id)
    if not db_item:
        return False
    session.delete(db_item)
    session.commit()
    return True
```

### 4.6 Файл routers/items.py (маршруты)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud
from app.models import ItemCreate, ItemRead, ItemUpdate
from app.database import SessionLocal

router = APIRouter(prefix="/items", tags=["items"])

# Dependency для получения сессии БД
def get_session():
    with SessionLocal() as session:
        yield session

# CREATE
@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    session: Session = Depends(get_session)
):
    return crud.create_item(session, item)

# READ (список)
@router.get("/", response_model=list[ItemRead])
async def list_items(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    return crud.get_items(session, skip=skip, limit=limit)

# READ (один)
@router.get("/{item_id}", response_model=ItemRead)
async def read_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    item = crud.get_item(session, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# UPDATE
@router.put("/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    session: Session = Depends(get_session)
):
    updated_item = crud.update_item(session, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

# DELETE
@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    session: Session = Depends(get_session)
):
    success = crud.delete_item(session, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
```

---

## 5. Работа с базой данных

### 5.1 SQL операторы
- **SELECT** - выборка данных
- **OFFSET (skip)** - пропустить N записей (для пагинации)
- **LIMIT** - ограничить количество результатов

**Пример:**
```python
# Если найдено 100 записей:
# offset=0, limit=10 → берем первые 10
# offset=30, limit=10 → пропускаем 30, берем следующие 10
# offset=20, limit=10 → с 31-го по 36-й (если всего 36)
```

### 5.2 Асинхронная работа с БД

Для асинхронных операций с базой данных используются AsyncEngine и AsyncSession из SQLAlchemy:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Асинхронный engine
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная сессия
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Использование в роутах
@router.get("/items")
async def get_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item))
    return result.scalars().all()
```

---

## 6. Миграции базы данных (Alembic)

### 6.1 Установка и инициализация
```bash
pip install alembic

# Инициализация (создает папку alembic/)
alembic init alembic

# Для асинхронных БД
alembic init -t async alembic
```

### 6.2 Настройка Alembic

**Файл alembic.ini:**
```ini
[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///./app.db
```

**Файл alembic/env.py:**
```python
from app.database import Base
from app.models import Item  # Импорт всех моделей

# Установка метаданных
target_metadata = Base.metadata

# Для использования переменных окружения
import os
from dotenv import load_dotenv

load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

### 6.3 Команды Alembic
```bash
# Создать миграцию автоматически
alembic revision --autogenerate -m "Initial migration"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Показать текущую версию
alembic current

# История миграций
alembic history
```

### 6.4 Запуск миграций при старте приложения
```python
from contextlib import asynccontextmanager
from alembic.config import Config
from alembic import command

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)
```

---

## 7. Автоматическая документация

### 7.1 Доступ к документации
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 7.2 Информация в документации
Документация автоматически генерируется на основе:
- Аннотаций типов
- Pydantic моделей
- Docstrings функций
- Параметров FastAPI (title, description, version)

### 7.3 Интерактивное тестирование
В Swagger UI можно:
1. Просмотреть все эндпоинты
2. Увидеть схемы данных
3. Протестировать API прямо в браузере (кнопка "Try it out")
4. Выполнить запросы и увидеть ответы

---

## 8. Тестирование

### 8.1 Пример базового теста
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_read_item():
    # Создание
    response = client.post(
        "/items/",
        json={"title": "Test Item", "price": 100.0}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    item_id = data["id"]
    
    # Чтение
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Item"
```

---

## 9. Продвинутые возможности

### 9.1 Dependency Injection
FastAPI использует систему внедрения зависимостей для управления общей логикой, такой как аутентификация и сессии базы данных:

```python
from fastapi import Depends

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Логика получения пользователя
    return user

@router.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    return user
```

### 9.2 Аутентификация и авторизация
FastAPI имеет встроенную интеграцию с OAuth2, JWT и OpenID Connect:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users/me")
async def read_current_user(token: str = Depends(oauth2_scheme)):
    return {"token": token}
```

### 9.3 Фильтрация и пагинация
```python
@router.get("/items")
async def get_items(
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    sort_by: str = "id",
    session: Session = Depends(get_session)
):
    query = select(Item)
    
    # Поиск
    if search:
        query = query.where(Item.title.like(f"%{search}%"))
    
    # Сортировка
    if sort_by == "price":
        query = query.order_by(Item.price)
    
    # Пагинация
    query = query.offset(skip).limit(limit)
    
    result = await session.execute(query)
    return result.scalars().all()
```

### 9.4 Валидация владельца
```python
@router.put("/{item_id}")
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    db_item = await session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Проверка владельца
    if db_item.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Обновление...
```

---

## 10. Преимущества и недостатки FastAPI

### 10.1 Преимущества
FastAPI предлагает высокую производительность благодаря асинхронным возможностям, автоматическую генерацию документации, встроенную валидацию данных и простоту изучения

1. **Высокая производительность** - сравнима с Node.js и Go
2. **Автоматическая документация** - Swagger UI из коробки
3. **Валидация данных** - через Pydantic
4. **Асинхронность** - нативная поддержка async/await
5. **Type hints** - автодополнение в IDE
6. **Быстрая разработка** - увеличение скорости разработки на 200-300%
7. **Меньше багов** - сокращение ошибок разработчика примерно на 40%

### 10.2 Недостатки
К недостаткам относятся централизация кода в main.py файле, отсутствие встроенной поддержки синглтонов в Dependency Injection и кривая обучения для асинхронного программирования

1. **Ручная структура** - нужно создавать файлы вручную
2. **Меньше встроенных инструментов** - нет админки, ORM (как в Django)
3. **Сложность асинхронности** - для новичков может быть трудно
4. **Меньшая экосистема** - меньше плагинов по сравнению с Flask/Django
5. **Централизация в main.py** - может привести к хаосу в больших проектах

---

## 11. Практические задачи

### Задачи для практики:
1. **Добавить поле owner_id** типа int и реализовать фильтрацию по владельцу
2. **Добавить проверку**, что только владелец может редактировать и удалять свои items
3. **Подключить Alembic** и создать первую миграцию
4. **Добавить пагинацию**, сортировку и поиск по названию
5. **Переписать работу с БД в асинхронном стиле** (если остается время)

---

## 12. Дополнительные ресурсы

### 12.1 Официальная документация
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Alembic: https://alembic.sqlalchemy.org/

### 12.2 Полезные библиотеки
- **FastAPI Users** - готовая система управления пользователями
- **Typer** - CLI-приложения (от создателя FastAPI)
- **SQLModel** - упрощенная работа с SQL
- **asyncpg** - асинхронный драйвер для PostgreSQL
- **aiomysql** - асинхронный драйвер для MySQL

### 12.3 Примеры использования
FastAPI используется для создания бэкендов веб и мобильных приложений, развертывания моделей машинного обучения, приложений реального времени с WebSockets

---

## 13. Заключение

FastAPI — это современный высокопроизводительный фреймворк, который обрабатывает более 3000 запросов в секунду. Он идеально подходит для:
- Микросервисной архитектуры
- API с высокой нагрузкой
- Реализации машинного обучения
- Real-time приложений
- Интеграции с современными frontend-фреймворками (React, Vue)

Основное отличие от Django — максимальная гибкость и асинхронность, но требует больше ручной работы при настройке проекта.