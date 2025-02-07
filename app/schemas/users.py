from fastapi_users import schemas
from typing import Optional

class UserRead(schemas.BaseUser[int]):
    """Schema for reading user data.

    Inherits from `BaseUser` and includes additional fields specific to the application.
    """

    name: str
    """The name of the user."""


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a new user.

    Inherits from `BaseUserCreate` and includes additional fields required during user creation.
    """

    name: str
    """The name of the user."""


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating an existing user.

    Inherits from `BaseUserUpdate` and includes optional fields that can be updated.
    """

    name: Optional[str] = None
    """The updated name of the user. Optional."""