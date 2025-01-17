from .conftest import client
from app.auth.auth import UserManager
import pytest
from unittest.mock import AsyncMock, patch
from app.db import get_async_session, get_user_db
from app.models.models import User
from app.schemas.users import UserRead
from app.auth.auth import auth_backend

@pytest.fixture(scope="module")
def db_test():
    pass


@pytest.mark.asyncio
async def test_create_user(client):
    # Define test user data
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
        print(response.json())
        assert response.status_code == 200

        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

