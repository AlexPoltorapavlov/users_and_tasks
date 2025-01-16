from .conftest import client
from app.auth.auth import UserManager
import pytest
from unittest.mock import AsyncMock, patch
from app.db import get_async_session
from app.models.models import User
from app.schemas.users import UserRead
from app.auth.auth import auth_backend

@pytest.mark.asyncio
async def test_create_user(client):

    mock_user_manager = AsyncMock(spec=UserManager)
    mock_user_manager.create.return_value = User(id = 2,
                                                 name = "test",
                                                 tasks = [],
                                                 email = "test2@gmail.com",
                                                 hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$iRKZ1XhGsZkyZ3BnC32Kgw$VFBGwBZ6qkF9B1s0/Dy/H+bXPGnu2bstP0MzNxAzVgQ",
                                                 is_active = True,
                                                 is_superuser = False,
                                                 is_verified = False)

    mock_user = User(id = 1,
                     name = "test",
                     tasks = [],
                     email = "test@gmail.com",
                     hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$iRKZ1XhGsZkyZ3BnC32Kgw$VFBGwBZ6qkF9B1s0/Dy/H+bXPGnu2bstP0MzNxAzVgQ",
                     is_active = True,
                     is_superuser = True,
                     is_verified = False)

    print(auth_backend.__dict__)

    with patch('app.routes.users.is_admin', return_value=True), \
        patch('app.auth.auth.get_user_manager', return_value=mock_user_manager):

        response = client.post("/users", json={"name": "test",
                                               "email": "test@gmail.com",
                                               "password": "test"})

        assert response.status_code == 201

