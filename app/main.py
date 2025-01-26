import uvicorn
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI

# db imports
from .db import User, create_db_and_tables, get_async_session

# schemas import
from .schemas.users import UserCreate, UserRead, UserUpdate
from .schemas.tasks import TaskCreate, TaskRead, TaskUpdate

# auth
from .auth.auth import auth_backend, current_active_user, fastapi_users

# Repositories
from .repositories.task import TaskRepository

# sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

# routes
from app.routes import authenticated_router
from .routes.tasks import router as tasks_router
from .routes.users import router as users_router

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(authenticated_router)
app.include_router(tasks_router)
app.include_router(
    users_router,
    prefix='',
    tags=["users"]
)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", log_level="info")