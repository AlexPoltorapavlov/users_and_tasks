from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.tasks import TaskRead, TaskCreate, TaskUpdate
from ..schemas.users import UserRead
from ..dal.task import TaskRepository
from ..db import get_async_session
from ..auth.auth import current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).create_task(task_data=task, user_id=user.id)

@router.get("/")
async def get_all_tasks(user: UserRead = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).get_tasks(user.id)

@router.get("/{task_id}")
async def get_task(task_id: int,
                   user: UserRead = Depends(current_active_user),
                   session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).get_task_by_id(task_id, user.id)

@router.put("/{task_id}")
async def update_task(task_id: int,
                      task_data: TaskUpdate,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).update_task(task_id, task_data, user.id)

@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    return await TaskRepository(session).delete_task(task_id, user.id)

