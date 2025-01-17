import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from fastapi_users import FastAPIUsers, BaseUserManager
from app.auth.auth import (
    get_jwt_strategy,
    auth_backend,
    UserManager,
    get_user_manager,
    current_active_user,
)
from app.routes import authenticated_router
from app.models.models import User
from app.db import get_user_db
from app.config import config

from .conftest import app, mock_user_db

SECRET = config.JWT_SECRET_KEY

# Тестируем get_jwt_strategy
def test_get_jwt_strategy():
    strategy = get_jwt_strategy()
    assert isinstance(strategy, JWTStrategy)
    assert strategy.secret == config.JWT_SECRET_KEY
    assert strategy.lifetime_seconds == 3600

# Тестируем UserManager
@pytest.mark.asyncio
async def test_user_manager(mock_user_db):
    user_db = AsyncMock()
    user_manager = UserManager(user_db)

    # Создаем объект User с правильными полями
    user = User(
        id=1,
        email="test@example.com",
        name="test",
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$7HlWFmfWt5jJvk0xwHjqDw$rkE8ijI0NAuZVkEOlBAziopL5Jzmvvuc4A7DIPRfvHc",
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )

    request = MagicMock()

    # Тестируем on_after_register
    await user_manager.on_after_register(user, request)
    user_db.on_after_register.assert_called_once_with(user, request)  # Проверяем вызов с аргументами

    # Тестируем on_after_forgot_password
    await user_manager.on_after_forgot_password(user, "token", request)
    user_db.on_after_forgot_password.assert_called_once_with(user, "token", request)

    # Тестируем on_after_request_verify
    await user_manager.on_after_request_verify(user, "token", request)
    user_db.on_after_request_verify.assert_called_once_with(user, "token", request)

    # Тестируем parse_id
    assert user_manager.parse_id("123") == 123

# Тестируем аутентификацию
@pytest.mark.asyncio
async def test_auth_backend():
    transport = BearerTransport(tokenUrl="auth/jwt/login")
    strategy = get_jwt_strategy()
    backend = AuthenticationBackend(
        name="jwt",
        transport=transport,
        get_strategy=lambda: strategy,
    )
    assert backend.name == "jwt"
    assert isinstance(backend.transport, BearerTransport)
    assert isinstance(backend.get_strategy(), JWTStrategy)

# Тестируем endpoint /auth/jwt/login
@pytest.mark.asyncio
async def test_login_endpoint(client):
    test_user_data = {
        "id": 2,
        "name": "string",
        "tasks": [],
        "email": "user1@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$iRKZ1XhGsZkyZ3BnC32Kgw$VFBGwBZ6qkF9B1s0/Dy/H+bXPGnu2bstP0MzNxAzVgQ",
        "is_active": True,
        "is_superuser": True,
        "is_verified": False
    }

    mock_user = User(**test_user_data)

    # Mock the database
    test_db = AsyncMock()
    test_db.get = AsyncMock(return_value=mock_user)
    mock_user_manager = UserManager(test_db)

    # Make the login request
    login_data = {
        "username": "user1@example.com",
        "password": "string"
    }

    with patch("app.auth.auth.get_user_manager", return_value=mock_user_manager):
        response = client.post("/auth/jwt/login", data=login_data)
        print(response.json())
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_current_active_user(client):
    test_user_data = {
        "id": 2,
        "name": "string",
        "tasks": [],
        "email": "user1@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$iRKZ1XhGsZkyZ3BnC32Kgw$VFBGwBZ6qkF9B1s0/Dy/H+bXPGnu2bstP0MzNxAzVgQ",
        "is_active": True,
        "is_superuser": True,
        "is_verified": False
    }

    mock_user = User(**test_user_data)

    # Mock the database
    test_db = AsyncMock()
    test_db.get = AsyncMock(return_value=mock_user)
    mock_user_manager = UserManager(test_db)

    # Make the login request
    login_data = {
        "username": "user1@example.com",
        "password": "string"
    }

    with patch('app.auth.auth.get_user_manager', return_value=mock_user_manager):
        response = client.post("/auth/jwt/login", data=login_data)
        auth_token = response.json()["access_token"]
        print(auth_token)
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/authenticated-route", headers=headers)
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"message": "You are authenticated", "user_id": 2}


