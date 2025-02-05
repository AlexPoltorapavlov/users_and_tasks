from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from app.schemas.users import UserCreate, UserRead
from app.auth.auth import current_active_user, get_user_manager
from fastapi_users.exceptions import UserAlreadyExists

router = APIRouter()

def is_admin(user = Depends(current_active_user)):
    """
    Dependency function to check if the current user has admin privileges.

    Args:
        user: Current authenticated user, injected by FastAPI

    Returns:
        bool: True if user is a superuser, False otherwise
    """
    return True if user.is_superuser else False

@router.post('/users')
async def user_create(user_data: UserCreate,
                      admin = Depends(is_admin),
                      user_manager = Depends(get_user_manager)):
    """
    Create a new user in the system.

    This endpoint is restricted to admin users only. It allows creation of new users
    with specified credentials and permissions.

    Args:
        user_data (UserCreate): User data for creating new user
        admin (bool): Whether the current user is an admin
        user_manager: User manager instance for handling user operations

    Returns:
        UserRead: Created user data

    Raises:
        HTTPException: 
            - 403 if the user is not an admin
            - 409 if a user with the same credentials already exists

    Notes:
        - Only admin users can create new users
        - Email must be unique in the system
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
    """
    Retrieve all users in the system.

    This endpoint is restricted to admin users only. It returns a list of all
    registered users in the system.

    Args:
        user_manager: User manager instance for handling user operations
        admin (bool): Whether the current user is an admin

    Returns:
        list[UserRead]: List of all users in the system

    Raises:
        HTTPException: 403 if the user is not an admin

    Notes:
        - Only admin users can access this endpoint
        - Returns all users regardless of their status
    """
    if admin:
        result = await user_manager.get_all()
        return result
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="The appropriate level of execution permission has not been granted.")

