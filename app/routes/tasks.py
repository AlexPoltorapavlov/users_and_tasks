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
    """Create a new task.

    Args:
        task (TaskCreate): The task data to be created.
        user (UserRead): The authenticated user, automatically injected by the `current_active_user` dependency.
        session (AsyncSession): The async database session, automatically injected by the `get_async_session` dependency.

    Returns:
        TaskRead: The newly created task.
    """
    return await TaskRepository(session).create_task(task_data=task, user_id=user.id)

@router.get("/")
async def get_all_tasks(user: UserRead = Depends(current_active_user),
                        session: AsyncSession = Depends(get_async_session)):
    """Retrieve all tasks for the authenticated user.

    Args:
        user (UserRead): The authenticated user, automatically injected by the `current_active_user` dependency.
        session (AsyncSession): The async database session, automatically injected by the `get_async_session` dependency.

    Returns:
        list[TaskRead]: A list of tasks associated with the authenticated user.
    """
    return await TaskRepository(session).get_tasks(user.id, user.is_superuser)

@router.get("/{task_id}")
async def get_task(task_id: int,
                   user: UserRead = Depends(current_active_user),
                   session: AsyncSession = Depends(get_async_session)):
    """Retrieve a specific task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.
        user (UserRead): The authenticated user, automatically injected by the `current_active_user` dependency.
        session (AsyncSession): The async database session, automatically injected by the `get_async_session` dependency.

    Returns:
        TaskRead | None: The task if found, otherwise None.
    """
    return await TaskRepository(session).get_task_by_id(task_id, user.id, user.is_superuser)

@router.put("/{task_id}")
async def update_task(task_id: int,
                      task_data: TaskUpdate,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    """Update an existing task.

    Args:
        task_id (int): The ID of the task to update.
        task_data (TaskUpdate): The updated task data.
        user (UserRead): The authenticated user, automatically injected by the `current_active_user` dependency.
        session (AsyncSession): The async database session, automatically injected by the `get_async_session` dependency.

    Returns:
        TaskRead | None: The updated task if found, otherwise None.
    """
    return await TaskRepository(session).update_task(task_id, task_data, user.id)

@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      user: UserRead = Depends(current_active_user),
                      session: AsyncSession = Depends(get_async_session)):
    """Delete a task by its ID.

    Args:
        task_id (int): The ID of the task to delete.
        user (UserRead): The authenticated user, automatically injected by the `current_active_user` dependency.
        session (AsyncSession): The async database session, automatically injected by the `get_async_session` dependency.

    Returns:
        TaskRead | None: The deleted task if found, otherwise None.
    """
    return await TaskRepository(session).delete_task(task_id, user.id)

