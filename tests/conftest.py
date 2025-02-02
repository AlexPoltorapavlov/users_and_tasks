# code from test_database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import get_async_session
from app.models import Base 
import pytest
from pytest_asyncio import fixture as async_fixture
from fastapi.testclient import TestClient

# Переопределение зависимости к сессиям для app
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Асинхронный генератор для тестовой сессии
async def override_get_async_session():
    """
    Функция для замены настоящего get_async_session
    """
    async with TestingSessionLocal() as session:
        yield session

@async_fixture(scope="module", autouse=True)
async def setup_db():
    """
    Создает таблицы в начале теста и удаляет в конце
    """
    # Создаём таблицы перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Удаляем таблицы после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
def get_client():
    # Переопределяем get_async_session перед тем, как получить клиент
    app.dependency_overrides[get_async_session] = override_get_async_session
    # Создаём клиент после переопределения зависимостей
    with TestClient(app) as client:
        print(type(client))
        return client

@pytest.fixture(scope="function")
def make_test_user(get_client):
    """
    Создаёт тестового пользователя через post запрос
    Args: get_client (fixture)
    Returns: user_data (dict)
    """
    user_data = {
        "email": "test@example.com",
        "password": "password",
        "name": "Test User"
    }
    client = get_client
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    return user_data

@pytest.fixture(scope="function")
def get_test_user():
    """
    Получаем данные для авторизации в формате dict
    """
    user_data = {
        "email": "test@example.com",
        "password": "password",
        "name": "Test User"
    }
    return user_data

@pytest.fixture(scope="function")
def token(get_client, get_test_user):
    """
    Получаем токен для действий авторизованных пользователей
    """
    client = get_client
    test_user = get_test_user
    response = client.post(
        "/auth/jwt/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
            "grant_type": "password"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]