import uuid
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from database import User, get_user_db
from config import config

SECRET = config.JWT_SECRET_KEY

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

