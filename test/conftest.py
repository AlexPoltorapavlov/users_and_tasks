import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from fastapi import FastAPI
import fastapi_users
from app.auth.auth import auth_backend
from app.routes import authenticated_router
from app.schemas.users import *

from app.auth.auth import (
    fastapi_users,
)

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