from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import get_async_session
from app.models.base_model import Base
from app.models import User
import pytest
from pytest_asyncio import fixture as async_fixture
from fastapi.testclient import TestClient
import os

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False,
    autoflush=False
)

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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    if os.path.exists("test_db.db"):
        os.remove("test_db.db")

@pytest.fixture(scope="function")
def get_client():
    app.dependency_overrides[get_async_session] = override_get_async_session
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