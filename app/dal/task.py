from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.models import Task
from ..schemas.tasks import *

class TaskRepository:
    """Repository class for handling database operations related to tasks."""

    def __init__(self,
                 session: AsyncSession,
                 task_table: Task):
        """Initializes the TaskRepository with an async database session.

        Args:
            session (AsyncSession): The async SQLAlchemy session for database operations.
            task_table (Base(SQLAlchemy.orm.DeclarativeBase)): The task's model
        """
        self.session = session
        self.task_table = task_table

    async def create_task(self, task_data: TaskCreate):
        """Creates a new task in the database.

        Args:
            task_data (TaskCreate): The task data to be created.
            user_id (int): The ID of the user creating the task.

        Returns:
            Task: The newly created task object.
        """
        task = self.task_table(**task_data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_tasks(self, user_id: int):
        """Retrieves all tasks associated with a specific user.

        Args:
            user_id (int): The ID of the user whose tasks are to be retrieved.
            is_admin (bool): The role of user

        Returns:
            list[Task]: A list of task objects associated with the user or all task objects if user is admin.
        """
        result = await self.session.execute(select(self.task_table).where(self.task_table.user_id == user_id))
        return result.scalars().all()

    async def get_all_tasks(self):
        """Retrieves all tasks from the database.

        Returns:
            list[Task]: A list of all task objects.
        """
        result = await self.session.execute(select(self.task_table))
        return result.scalars().all()

    async def get_task_by_id(self, task_id: int, user_id: int):
        """Retrieves a specific task by its ID and user ID.

        Args:
            task_id (int): The ID of the task to retrieve.
            user_id (int): The ID of the user associated with the task.
            is_admin (bool): The role of user

        Returns:
            Task | None: The task object if found, otherwise None.
        """
        result = await self.session.execute(select(self.task_table).where(self.task_table.id == task_id, self.task_table.user_id == user_id))
        task = result.scalar_one_or_none()
        return task if task else None

    async def get_specific_task_by_id(self, task_id: int):
        """Retrieves a specific task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Task | None: The task object if found, otherwise None.
        """
        result = await self.session.execute(select(self.task_table).where(self.task_table.id == task_id))
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

    async def update_specific_task(self, task_id: int, task_data: TaskUpdate):
        """Updates an existing task in the database.

        Args:
            task_id (int): The ID of the task to update.
            task_data (TaskUpdate): The updated task data.

        Returns:
            Task | None: The updated task object if found, otherwise None.
        """
        task = await self.get_specific_task_by_id(task_id)
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

    async def delete_specific_task(self, task_id: int):
        """Deletes a task from the database.

        Args:
            task_id (int): The ID of the task to delete.

        Returns:
            Task | None: The deleted task object if found, otherwise None.
        """
        task = await self.get_specific_task_by_id(task_id)
        if task is None:
            return None

        await self.session.delete(task)
        await self.session.commit()
        return task




