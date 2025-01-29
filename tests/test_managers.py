import pytest_asyncio
import pytest
from app.managers.task import TaskManager, get_task_manager
from .mock_repositories import *
from app.schemas.tasks import *


@pytest.mark.asyncio
async def test_get_task_manager(mock_get_task_repository):
    task_manager_generator = get_task_manager(mock_get_task_repository)
    task_manager = await task_manager_generator.__anext__()
    assert isinstance(task_manager, TaskManager)

@pytest.mark.asyncio
async def test_create_task(mock_get_task_manager):
    task_manager = mock_get_task_manager
    task_data = TaskCreate(
        name="Test Task",
        description="Test Description",
        status="new",
        user_id=1  # Убедитесь, что user_id передается, если требуется
    )
    
    result = await task_manager.create_task(task_data)
    
    # Проверяем, что метод create_task репозитория был вызван
    task_manager.task_db.create_task.assert_awaited_once_with(task_data)
    
    # Проверяем, что результат соответствует ожиданиям
    assert isinstance(result, TaskRead)
    assert result.id == 1
    assert result.name == "Test Task"

@pytest.mark.asyncio
async def test_create_task_invalid_data(mock_get_task_manager):
    task_manager = mock_get_task_manager 
    with pytest.raises(ValidationError):
        task_data = TaskCreate(
            name="Test Task",
            description="Test Description",
            status="invalid_status", # status must be "new", "in_progress", "completed"
            user_id=1
        )

