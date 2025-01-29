from pytest_asyncio import fixture as async_fixture
import pytest
from app.repositories import TaskRepository
from unittest.mock import AsyncMock
from app.models import Task, User
from app.managers.task import TaskManager

#########
# Фикстуры с задачами
#########

@pytest.fixture
def get_base_task():
    mock_task = Task(
        id=1,
        name="Test Task",
        description="Test Description",
        status="new",
        user_id=1
    )
    return mock_task

@pytest.fixture
def get_update_task():
    mock_task = Task(
        id=1,
        name="Updated Test Task",
        description="Updated Test Description",
        status="in_progress",
        user_id=1
    )
    return mock_task

##########
# Фикстуры для получения объекта TaskManager
##########

@async_fixture
async def task_repository(get_base_task):
    """
    Args: 
        get_base_task(pytest.fixture) with base task example
        
    Returning: task_repository (AsyncMock) - mock of TaskRepository object
    """

    task_repository = AsyncMock(spec=TaskRepository)
    base_task = get_base_task
    task_repository.create_task = AsyncMock(return_value=base_task)
    return task_repository

@async_fixture
async def mock_get_task_repository(task_repository):
    return task_repository

@async_fixture
async def mock_get_task_manager(mock_get_task_repository):
    return TaskManager(mock_get_task_repository)
