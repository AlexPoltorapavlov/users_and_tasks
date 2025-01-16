# System
import os

# Database
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from collections.abc import AsyncGenerator

# Testing
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch

# fastapi
from fastapi import FastAPI
import fastapi_users

# Local modules
from app.auth.auth import auth_backend
from app.routes import authenticated_router
from app.routes.tasks import router as tasks_router
from app.routes.users import router as users_router
from app.schemas.users import *
from app.auth.auth import fastapi_users
from app.models.models import Base
from app.db import get_async_session

@pytest.fixture
def mock_user_db():
    """Фикстура для мокирования зависимости `get_user_db`.

    Returns:
        MagicMock: Мок объект для `get_user_db`.
    """
    with patch("app.db.get_user_db") as mock:
        yield mock


@pytest.fixture
def mock_user_manager(mock_user_db):
    """Фикстура для мокирования `UserManager`.

    Args:
        mock_user_db (MagicMock): Мок объект для `get_user_db`.

    Returns:
        MagicMock: Мок объект для `UserManager`.
    """
    with patch("app.auth.auth.UserManager") as mock:
        yield mock


@pytest.fixture
def app():
    """Фикстура для создания тестового приложения FastAPI.

    Returns:
        FastAPI: Тестовое приложение FastAPI с подключенными маршрутами.
    """
    app = FastAPI()
    app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt")
    app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth")
    app.include_router(authenticated_router)
    app.include_router(tasks_router)
    app.include_router(users_router)
    return app


@pytest.fixture
def client(app):
    """Фикстура для создания тестового клиента FastAPI.

    Args:
        app (FastAPI): Тестовое приложение FastAPI.

    Returns:
        TestClient: Тестовый клиент для отправки HTTP-запросов.
    """
    return TestClient(app)

@pytest.fixture(scope="session")
def db_file():
    """Фикстура для создания временного файла базы данных SQLite.

    Returns:
        str: Путь к временному файлу базы данных.

    После завершения тестовой сессии файл базы данных удаляется, если он существует.
    """
    db_path = "test_database.db"
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest_asyncio.fixture(scope="session")
async def engine(db_file):
    """Фикстура для создания асинхронного движка SQLAlchemy.

    Args:
        db_file (str): Путь к файлу базы данных.

    Returns:
        AsyncEngine: Асинхронный движок SQLAlchemy.

    После завершения тестовой сессии движок корректно закрывается.
    """
    DATABASE_URL = f"sqlite+aiosqlite:///{db_file}"
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def create_db_and_tables(engine):
    """Фикстура для создания всех таблиц в базе данных.

    Args:
        engine (AsyncEngine): Асинхронный движок SQLAlchemy.

    Выполняет создание всех таблиц, определенных в `Base.metadata`.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def async_session_maker(engine):
    """Фикстура для создания фабрики асинхронных сессий.

    Args:
        engine (AsyncEngine): Асинхронный движок SQLAlchemy.

    Returns:
        async_sessionmaker: Фабрика для создания асинхронных сессий.
    """
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture()
async def session(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для создания асинхронной сессии.

    Args:
        async_session_maker (async_sessionmaker): Фабрика для создания асинхронных сессий.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.

    После завершения теста сессия автоматически закрывается.
    """
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture()
async def test_db(create_db_and_tables, session):
    """Фикстура для предоставления асинхронной сессии для тестов.

    Args:
        create_db_and_tables: Фикстура, создающая таблицы в базе данных.
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        AsyncSession: Асинхронная сессия для выполнения операций с базой данных.
    """
    return session