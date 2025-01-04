from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from config import config
import uuid
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from app.db import User, get_user_db
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


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user, request = None):
        return await super().on_after_register(user, request)
    
    async def on_after_forgot_password(self, user, token, request = None):
        return await super().on_after_forgot_password(user, token, request)
    
    async def on_after_request_verify(self, user, token, request = None):
        return await super().on_after_request_verify(user, token, request)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

