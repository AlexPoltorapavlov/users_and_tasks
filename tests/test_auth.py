import pytest
from app.auth.auth import (
    UserManager,
    get_jwt_strategy,
    get_user_manager,
    fastapi_users
)
from fastapi import Depends
from fastapi.exceptions import HTTPException
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi_users.db import BaseUserDatabase
from tests import conftest

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
    mock_user_repository = AsyncMock()
    mock_user_repository.get_all_users.return_value = []
    user_manager = UserManager(user_db=mock_user_repository)

    result = await user_manager.get_all_users()
    assert isinstance(user_manager, UserManager)
    assert result == []

@pytest.mark.asyncio
async def test_get_user_manager_returns_user_manager():
    mock_user_db = MagicMock()
    mock_get_user_db = MagicMock(return_value=mock_user_db)

    with patch('app.auth.auth.get_user_db', mock_get_user_db):
        user_manager_generator = get_user_manager()
        user_manager = await anext(user_manager_generator)

        assert isinstance(user_manager, UserManager)
        assert user_manager.user_db == mock_user_db

    mock_get_user_db.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_manager_with_exception_in_dependency():
    def mock_get_user_db():
        raise HTTPException(status_code=500, detail="Database error")

    with pytest.raises(HTTPException):
        async for _ in get_user_manager(Depends(mock_get_user_db)):
            pass


@pytest.mark.asyncio
async def test_get_user_manager_with_invalid_input():
    with pytest.raises(TypeError):
        async for _ in get_user_manager("invalid_input"):
            pass


@pytest.mark.asyncio
async def test_get_user_manager_with_invalid_user_db():
    invalid_user_db = object()  # An object that doesn't have the required methods

    with pytest.raises(AttributeError):
        async for user_manager in get_user_manager(invalid_user_db):
            await user_manager.get_all_users()


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