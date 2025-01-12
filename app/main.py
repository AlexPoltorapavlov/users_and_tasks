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
from .dal.task import TaskRepository

# sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

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


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

@app.post("/tasks", response_model=TaskRead)
async def create_task(task: TaskCreate,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).create_task(task_data=task, user_id=user.id)

@app.get("/tasks")
async def get_all_tasks(user: UserRead = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).get_tasks(user.id)

@app.get("/tasks/{task_id}" )
async def get_task(task_id: int,
                   user: UserRead = Depends(current_active_user),
                   session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).get_task_by_id(task_id, user.id)

@app.put("/tasks/{task_id}")
async def update_task(task_id: int,
                      task_data: TaskUpdate,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).update_task(task_id, task_data, user.id)

@app.delete("/tasks/{task_id}", response_model=TaskRead)
async def delete_task(task_id: int,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).delete_task(task_id, user.id)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", log_level="info")