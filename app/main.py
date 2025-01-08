import uvicorn

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

# db imports
from .db import User, create_db_and_tables, get_async_session

# schemas import
from .schemas.users import UserCreate, UserRead, UserUpdate
from .schemas.tasks import TaskCreate, TaskRead, TaskUpdate, TaskBase

# auth
from .auth.auth import auth_backend, current_active_user, fastapi_users

# Repositories
from .dal.task import TaskRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

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


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.post("/tasks", response_model=TaskRead)
async def create_task(task: TaskBase,
                      user: UserRead = Depends(current_active_user),
                      session = Depends(get_async_session)):
    return await TaskRepository(session).create_task(task_data=task, user_id=user.id)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", log_level="info")