from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from app.schemas.users import UserCreate, UserRead
from app.models.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.auth.auth import current_active_user, get_user_manager
from fastapi_users.exceptions import UserAlreadyExists

router = APIRouter()

def is_admin(user = Depends(current_active_user)):
    """Check if the authenticated user is an admin.

    Args:
        user (UserRead): The authenticated user, automatically injected by the `current_active_user` dependency.

    Returns:
        bool: True if the user is a superuser (admin), otherwise False.
    """
    return True if user.is_superuser else False

@router.post('/users')
async def user_create(user_data: UserCreate,
                      admin = Depends(is_admin),
                      user_manager = Depends(get_user_manager)):
    """Create a new user (admin-only endpoint).

    Args:
        user_data (UserCreate): The user data to be created.
        admin (bool): Whether the authenticated user is an admin, automatically injected by the `is_admin` dependency.
        user_manager: The user manager instance, automatically injected by the `get_user_manager` dependency.

    Returns:
        UserRead: The newly created user.

    Raises:
        HTTPException:
            - 403: If the authenticated user is not an admin.
            - 409: If a user with the same email or username already exists.
    """
    if admin:
        try:
            user = await user_manager.create(user_data)
            return UserRead.model_validate(user)
        except UserAlreadyExists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User already exist")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="The appropriate level of execution permission has not been granted.")


@router.get('/users')
async def get_users(user_manager = Depends(get_user_manager),
                    admin = Depends(is_admin)):
    if admin:
        result = await user_manager.get_all()
        return result
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="The appropriate level of execution permission has not been granted.")

