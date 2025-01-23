from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from sqlalchemy import select
from ..config import config
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers

from app.models.models import User
from app.db import get_user_db

from typing import Optional, List

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

SECRET = config.JWT_SECRET_KEY

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")  # Логирование для отладки
        # Вызываем метод из user_db, если он есть
        if hasattr(self.user_db, 'on_after_register'):
            await self.user_db.on_after_register(user, request)
        else:
            await super().on_after_register(user, request)  # Вызов родительского метода

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has requested a password reset.")
        if hasattr(self.user_db, 'on_after_forgot_password'):
            await self.user_db.on_after_forgot_password(user, token, request)
        else:
            await super().on_after_forgot_password(user, token, request)

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has requested a verification.")
        if hasattr(self.user_db, 'on_after_request_verify'):
            await self.user_db.on_after_request_verify(user, token, request)
        else:
            await super().on_after_request_verify(user, token, request)

    async def get_all_users(self):
        return await self.user_db.get_all_users()
    def parse_id(self, value):
        return int(value)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

