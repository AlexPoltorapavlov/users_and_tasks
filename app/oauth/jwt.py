from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from config import config

bearer_transport = BearerTransport(tokenUrl="oauth/jwt/login")

SECRET = config.JWT_SECRET_KEY

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

oauth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)