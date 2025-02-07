from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.models import Task, User

async def get_user_repository(session: AsyncSession = Depends(get_async_session)):
    """Dependency function to provide a `SQLAlchemyUserDatabase` instance.

    Args:
        session (AsyncSession): The async SQLAlchemy session, injected by the `get_async_session` dependency.

    Returns:
        SQLAlchemyUserDatabase: An instance of `SQLAlchemyUserDatabase` for managing user-related database operations.
    """
    yield UserRepository(session, User)

async def get_task_repository(session: AsyncSession = Depends(get_async_session)):
    """Dependency function to provide a TaskRepository instance with an async session.

    Args:
        session (AsyncSession): The async SQLAlchemy session (injected by FastAPI).

    Yields:
        TaskRepository: An instance of TaskRepository for handling task-related database operations.
    """
    yield TaskRepository(session, Task, User)

__all__ = ["TaskRepository",
           "UserRepository",
           "get_user_repository",
           "get_task_repository"]
