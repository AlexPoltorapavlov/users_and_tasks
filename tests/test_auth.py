import pytest
from unittest.mock import patch

@pytest.fixture(scope="function")
def mock_user():
    from app.auth.auth import User
    return User(id=1, email="test@test.com", hashed_password="hashed_password", is_active=True, is_superuser=False, is_verified=False)

def test_get_jwt_strategy():
    from app.auth.auth import get_jwt_strategy
    SECRET = "SECRET"

    with patch("app.auth.auth.SECRET", SECRET):
        jwt_strategy = get_jwt_strategy()
        assert jwt_strategy.secret == "SECRET"
        assert jwt_strategy.lifetime_seconds == 3600
        assert jwt_strategy.token_audience == ["fastapi-users:auth"]
        assert jwt_strategy.algorithm == "HS256"

def test_parse_id(mock_user):
    from app.auth.auth import UserManager
    user_manager = UserManager(mock_user)

    assert user_manager.parse_id(2) == 2
    assert user_manager.parse_id("2") == 2

    with pytest.raises(ValueError):
        user_manager.parse_id("a")
    with pytest.raises(ValueError):
        user_manager.parse_id("2.0")
    with pytest.raises(TypeError):
        user_manager.parse_id()