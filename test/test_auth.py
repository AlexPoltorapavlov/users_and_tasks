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
    fastapi_users,
    current_active_user,
)
from app.routes import authenticated_router
from app.models.models import User
from app.db import get_user_db
from app.config import config
from app.schemas.users import UserCreate, UserRead, UserUpdate

SECRET = config.JWT_SECRET_KEY

# Мокируем зависимости
@pytest.fixture
def mock_user_db():
    with patch("app.db.get_user_db") as mock:
        yield mock

@pytest.fixture
def mock_user_manager(mock_user_db):
    with patch("app.auth.auth.UserManager") as mock:
        yield mock

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt")
    app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth")
    app.include_router(authenticated_router)
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

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
    # Mock UserManager
    user_manager = AsyncMock()
    user_manager.authenticate.return_value = User(
        id=1,
        email="test@example.com",
        is_active=True,
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$jnx9MxgXVPQi2v4qPRqp0Q$lJALRPOTccij1hx7KQL0bsAfIpOftkn3tpAuvg9fbGU",
        is_superuser=False,
        is_verified=False,
    )

    login_data = {
        "username": "user@example.com",
        "password": "string"
    }
    response = client.post("/auth/jwt/login", data=login_data)
    print(response.json())
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_current_active_user(client):
    user = User(
        id=1,
        email="test@example.com",
        is_active=True,
        hashed_password="$argon2id$v=19$m=65536,t=3,p=4$jnx9MxgXVPQi2v4qPRqp0Q$lJALRPOTccij1hx7KQL0bsAfIpOftkn3tpAuvg9fbGU",
        is_superuser=False,
        is_verified=False,
    )

    user_manager = AsyncMock()
    user_manager.get_current_user.return_value = user
    
    print(user.id)

    # Generate a valid JWT token
    from app.auth.auth import get_jwt_strategy
    strategy = get_jwt_strategy()
    token = await strategy.write_token(user)

    response = client.get("/authenticated-route", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "You are authenticated", "user_id": 1}