from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from sqlalchemy import select
from ..config import config
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from app.repositories.user import UserRepository

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
    """
    User management class that handles user-related operations like registration,
    password reset, and verification.

    Inherits from BaseUserManager and specializes for User model with integer IDs.

    Attributes:
        reset_password_token_secret (str): Secret key used for password reset tokens
        verification_token_secret (str): Secret key used for verification tokens
    """

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Callback that runs after a user has been registered.

        Args:
            user (User): The newly registered user instance
            request (Optional[Request]): The FastAPI request object, if available

        Note:
            Logs registration event and delegates to user_db handler if available
        """
        if hasattr(self.user_db, 'on_after_register'):
            await self.user_db.on_after_register(user, request)
        else:
            await super().on_after_register(user, request)

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        """
        Callback that runs after a user has been registered.

        Args:
            user (User): The newly registered user instance
            request (Optional[Request]): The FastAPI request object, if available

        Note:
            Logs registration event and delegates to user_db handler if available
        """
        if hasattr(self.user_db, 'on_after_forgot_password'):
            await self.user_db.on_after_forgot_password(user, token, request)
        else:
            await super().on_after_forgot_password(user, token, request)

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        """
        Callback that runs after a user has requested email verification.

        Args:
            user (User): The user requesting verification
            token (str): The generated verification token
            request (Optional[Request]): The FastAPI request object, if available

        Note:
            Logs verification request and delegates to user_db handler if available
        """
        if hasattr(self.user_db, 'on_after_request_verify'):
            await self.user_db.on_after_request_verify(user, token, request)
        else:
            await super().on_after_request_verify(user, token, request)

    async def get_all(self):
        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of all users in the database
        """
        return await self.user_db.get_all()

    def parse_id(self, value):
        """
        Converts a user ID value to integer format.

        Args:
            value: The ID value to parse

        Returns:
            int: The parsed integer ID

        Note:
            Used for converting string IDs to integers when needed
        """
        return int(value)


async def get_user_manager(user_db: UserRepository = Depends(get_user_db)):
    if not isinstance(user_db, UserRepository):
        raise TypeError(f"Expected UserRepository, got {type(user_db).__name__}")
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

