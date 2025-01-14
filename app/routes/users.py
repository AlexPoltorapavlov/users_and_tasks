from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from app.schemas.users import UserCreate, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.auth.auth import current_active_user, get_user_manager
from fastapi_users.exceptions import UserAlreadyExists

router = APIRouter()

def is_admin(user = Depends(current_active_user)):
    return True if user.is_superuser else False

@router.post('/users')
async def user_create(user_data: UserCreate,
                      session: AsyncSession = Depends(get_async_session),
                      admin = Depends(is_admin),
                      user_manager = Depends(get_user_manager)):
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

