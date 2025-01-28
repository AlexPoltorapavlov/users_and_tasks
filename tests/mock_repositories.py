from pytest_asyncio import fixture as async_fixture
from app.repositories import TaskRepository
from unittest.mock import AsyncMock
from app.models import Task, User
from app.managers.task import TaskManager

@async_fixture
async def mock_get_task_repository():
    return AsyncMock(spec=TaskRepository)

@async_fixture
async def mock_get_task_manager(mock_get_task_repository):
    return TaskManager(mock_get_task_repository)