from app.repositories import TaskRepository
from app.db import get_task_db
from fastapi import Depends, HTTPException
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskRead
from app.errors.user_errors import UserNotFoundError

class TaskManager:
    """
    Manager class for handling task-related operations.
    
    This class provides methods for creating, retrieving, updating, and deleting tasks,
    with support for both user-specific and general task operations.

    Attributes:
        task_db (TaskRepository): Repository instance for task database operations
    """

    def __init__(self, task_db):
        """
        Initialize TaskManager with a task repository.

        Args:
            task_db (TaskRepository): Repository instance for task database operations
        """
        self.task_db = task_db

    async def create_task(self, task_data: TaskCreate):
        """
        Create a new task for a user.

        Args:
            task_data (TaskCreate): Data for creating the new task

        Returns:
            TaskRead: Created task data

        Raises:
            HTTPException: If the specified user is not found (404)
        """
        try:
            result = await self.task_db.create_task(task_data)
            return TaskRead(**result.__dict__) if result else None
        except UserNotFoundError:
            raise HTTPException(status_code=404, detail=f"User id: {task_data.user_id} not found")

    async def get_tasks(self, user_id: int):
        """
        Retrieve all tasks for a specific user.

        Args:
            user_id (int): ID of the user whose tasks to retrieve

        Returns:
            List[TaskRead]: List of tasks belonging to the user
        """
        results = await self.task_db.get_tasks(user_id)
        return [TaskRead(**task.__dict__) for task in results] if results else []

    async def get_all_tasks(self):
        """
        Retrieve all tasks in the system.

        Returns:
            List[TaskRead]: List of all tasks
        """
        results = await self.task_db.get_all_tasks()
        return [TaskRead(**task.__dict__) for task in results] if results else []

    async def get_task_by_id(self, task_id: int, user_id: int):
        """
        Retrieve a specific task for a user.

        Args:
            task_id (int): ID of the task to retrieve
            user_id (int): ID of the user who owns the task

        Returns:
            TaskRead: Task data if found, None otherwise
        """
        result = await self.task_db.get_task_by_id(task_id, user_id)
        return TaskRead(**result.__dict__) if result else None

    async def get_specific_task_by_id(self, task_id: int):
        """
        Retrieve a specific task by its ID regardless of user.

        Args:
            task_id (int): ID of the task to retrieve

        Returns:
            TaskRead: Task data if found, None otherwise
        """
        result = await self.task_db.get_specific_task_by_id(task_id)
        return TaskRead(**result.__dict__) if result else None

    async def update_task(self, task_id: int, task_data: TaskUpdate, user_id: int):
        """
        Update a specific task for a user.

        Args:
            task_id (int): ID of the task to update
            task_data (TaskUpdate): New task data
            user_id (int): ID of the user who owns the task

        Returns:
            TaskRead: Updated task data
        """
        result = await self.task_db.update_task(task_id, task_data, user_id)
        return TaskRead(**result.__dict__) if result else None

    async def update_specific_task(self, task_id: int, task_data: TaskUpdate):
        """
        Update a specific task regardless of user.

        Args:
            task_id (int): ID of the task to update
            task_data (TaskUpdate): New task data

        Returns:
            TaskRead: Updated task data
        """
        result = await self.task_db.update_specific_task(task_id, task_data)
        return TaskRead(**result.__dict__) if result else None

    async def delete_task(self, task_id: int, user_id: int):
        """
        Delete a specific task for a user.

        Args:
            task_id (int): ID of the task to delete
            user_id (int): ID of the user who owns the task

        Returns:
            TaskRead: Deleted task data
        """
        result = await self.task_db.delete_task(task_id, user_id)
        return TaskRead(**result.__dict__) if result else None

    async def delete_specific_task(self, task_id: int):
        """
        Delete a specific task regardless of user.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            TaskRead: Deleted task data
        """
        result = await self.task_db.delete_specific_task(task_id)
        return TaskRead(**result.__dict__) if result else None


async def get_task_manager(task_db: TaskRepository = Depends(get_task_db)):
    """
    FastAPI dependency that creates and yields a TaskManager instance.

    Args:
        task_db (TaskRepository): Repository for task operations, injected by FastAPI.
            Defaults to the result of get_task_db dependency.

    Yields:
        TaskManager: An instance of TaskManager configured with the provided TaskRepository.

    Raises:
        TypeError: If task_db is not an instance of TaskRepository.
    """
    if not isinstance(task_db, TaskRepository):
        raise TypeError(f"Expected TaskRepository, got {type(task_db).__name__}")
    yield TaskManager(task_db)

