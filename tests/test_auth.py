import pytest
from unittest.mock import patch

def test_get_jwt_strategy():
    from app.auth.auth import get_jwt_strategy
    SECRET = "SECRET"

    with patch("app.auth.auth.SECRET", SECRET):
        jwt_strategy = get_jwt_strategy()
        assert jwt_strategy.secret == "SECRET"
        assert jwt_strategy.lifetime_seconds == 3600
        assert jwt_strategy.token_audience == ["fastapi-users:auth"]
        assert jwt_strategy.algorithm == "HS256"