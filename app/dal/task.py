from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.models import Task
from ..schemas.tasks import *
from ..db import get_async_session

class TaskRepository:
    """Repository class for handling database operations related to tasks."""

    def __init__(self, session: AsyncSession):
        """Initializes the TaskRepository with an async database session.

        Args:
            session (AsyncSession): The async SQLAlchemy session for database operations.
        """
        self.session = session

    async def create_task(self, task_data: TaskCreate, user_id: int):
        """Creates a new task in the database.

        Args:
            task_data (TaskCreate): The task data to be created.
            user_id (int): The ID of the user creating the task.

        Returns:
            Task: The newly created task object.
        """
        task = Task(**task_data.model_dump(), user_id = user_id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_tasks(self, user_id: int, is_admin: bool = False):
        """Retrieves all tasks associated with a specific user.

        Args:
            user_id (int): The ID of the user whose tasks are to be retrieved.
            is_admin (bool): The role of user

        Returns:
            list[Task]: A list of task objects associated with the user or all task objects if user is admin.
        """
        if is_admin:
            result = await self.session.execute(select(Task))
            return result.scalars().all()
        else:
            result = await self.session.execute(select(Task).where(Task.user_id == user_id))
            return result.scalars().all()

    async def get_task_by_id(self, task_id: int, user_id: int, is_admin: bool = False):
        """Retrieves a specific task by its ID and user ID.

        Args:
            task_id (int): The ID of the task to retrieve.
            user_id (int): The ID of the user associated with the task.
            is_admin (bool): The role of user

        Returns:
            Task | None: The task object if found, otherwise None.
        """
        if is_admin:
            result = await self.session.execute(select(Task).where(Task.id == task_id))
            return result.scalar_one_or_none()
        else:
            result = await self.session.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
            task = result.scalar_one_or_none()
            return task if task else None

    async def update_task(self, task_id: int, task_data: TaskUpdate, user_id: int):
        """Updates an existing task in the database.

        Args:
            task_id (int): The ID of the task to update.
            task_data (TaskUpdate): The updated task data.
            user_id (int): The ID of the user associated with the task.

        Returns:
            Task | None: The updated task object if found, otherwise None.
        """
        task = await self.get_task_by_id(task_id, user_id)
        if task is None:
            return None

        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id: int, user_id: int):
        """Deletes a task from the database.

        Args:
            task_id (int): The ID of the task to delete.
            user_id (int): The ID of the user associated with the task.

        Returns:
            Task | None: The deleted task object if found, otherwise None.
        """
        task = await self.get_task_by_id(task_id, user_id)
        if task is None:
            return None
        
        await self.session.delete(task)
        await self.session.commit()
        return task


async def get_task_db(session: AsyncSession = Depends(get_async_session)):
    """Dependency function to provide a TaskRepository instance with an async session.

    Args:
        session (AsyncSession): The async SQLAlchemy session (injected by FastAPI).

    Yields:
        TaskRepository: An instance of TaskRepository for handling task-related database operations.
    """
    yield TaskRepository(session)