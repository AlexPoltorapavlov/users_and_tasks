import pytest
from app.auth.auth import (
    UserManager,
    get_jwt_strategy,
    get_user_manager,
    fastapi_users
)
from app.dal.user import UserRepository
from fastapi import Depends, HTTPException
from unittest.mock import patch, AsyncMock

def test_get_jwt_strategy():
    SECRET = "SECRET"

    with patch("app.auth.auth.SECRET", SECRET):
        jwt_strategy = get_jwt_strategy()
        assert jwt_strategy.secret == "SECRET"
        assert jwt_strategy.lifetime_seconds == 3600
        assert jwt_strategy.token_audience == ["fastapi-users:auth"]
        assert jwt_strategy.algorithm == "HS256"

@pytest.mark.asyncio
async def test_get_user_manager_edge_case_empty_user_db():
    mock_user_db = AsyncMock(spec=UserRepository)
    mock_user_db.get_all.return_value = []
    user_manager = UserManager(user_db=mock_user_db)

    result = await user_manager.get_all()
    assert isinstance(user_manager, UserManager)
    assert result == []

@pytest.mark.asyncio
async def test_get_user_manager_returns_user_manager():
    mock_user_db = AsyncMock(spec=UserRepository)

    with patch('app.auth.auth.get_user_db', return_value=mock_user_db):
        user_manager_generator = get_user_manager(mock_user_db)
        user_manager = await anext(user_manager_generator)

        assert isinstance(user_manager, UserManager)
        assert user_manager.user_db == mock_user_db


@pytest.mark.asyncio
async def test_get_user_manager_with_invalid_input():
    with pytest.raises(TypeError):
        async for _ in get_user_manager("invalid_input"):
            pass


@pytest.mark.asyncio
async def test_get_user_manager_with_invalid_user_db():
    invalid_user_db = object()

    with pytest.raises(TypeError):
        async for user_manager in get_user_manager(invalid_user_db):
            await user_manager.get_all()


@pytest.mark.asyncio
async def test_get_user_manager_with_none_input():
    with pytest.raises(TypeError):
        async for _ in get_user_manager(None):
            pass


def test_parse_id():
    mock_user_db = AsyncMock()
    user_manager = UserManager(mock_user_db)

    assert user_manager.parse_id(2) == 2
    assert user_manager.parse_id("2") == 2

    with pytest.raises(ValueError):
        user_manager.parse_id("a")
    with pytest.raises(ValueError):
        user_manager.parse_id("2.0")
    with pytest.raises(TypeError):
        user_manager.parse_id()