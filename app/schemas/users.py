from fastapi_users import schemas
from typing import Optional

class UserRead(schemas.BaseUser[int]):
    name: str

class UserCreate(schemas.BaseUserCreate):
    name: str

class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str]