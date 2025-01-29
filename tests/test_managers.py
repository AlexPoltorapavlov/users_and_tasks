import pytest_asyncio
import pytest
from app.managers.task import TaskManager, get_task_manager
from .mock_repositories import *
from app.schemas.tasks import *
from pydantic import ValidationError


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

@pytest.mark.asyncio
async def test_get_tasks(mock_get_task_manager):
    task_manager = mock_get_task_manager
    user_id = 1
    result = await task_manager.get_tasks(user_id) # must return list with 3 tasks
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], TaskRead)

@pytest.mark.asyncio
async def test_get_task_by_id(mock_get_task_manager):
    task_manager = mock_get_task_manager
    task_id, user_id = 1, 1
    result = await task_manager.get_task_by_id(task_id, user_id)
    assert isinstance(result, TaskRead)
    assert result.id == task_id

@pytest.mark.asyncio
async def test_update_task(mock_get_task_manager):
    task_manager = mock_get_task_manager
    task_id, user_id = 1, 1
    task_data = TaskUpdate(
        name="Updated Test Task",
        description="Updated Test Description",
        status="in_progress"
    )
    result = await task_manager.update_task(task_id, task_data, user_id)
    assert isinstance(result, TaskRead)
    assert result.id == task_id
    assert result.name == "Updated Test Task"

@pytest.mark.asyncio
async def test_delete_task(mock_get_task_manager):
    task_manager = mock_get_task_manager
    task_id, user_id = 1, 1
    result = await task_manager.delete_task(task_id, user_id)
    assert isinstance(result, TaskRead)
    assert result.id == task_id

@pytest.mark.asyncio
async def test_get_all_tasks(mock_get_task_manager):
    task_manager = mock_get_task_manager
    result = await task_manager.get_all_tasks()
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], TaskRead)

@pytest.mark.asyncio
async def test_get_specific_task_by_id(mock_get_task_manager):
    task_manager = mock_get_task_manager
    task_id = 1
    result = await task_manager.get_specific_task_by_id(task_id)
    assert isinstance(result, TaskRead)
    assert result.id == task_id