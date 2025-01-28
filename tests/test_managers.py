import pytest_asyncio
import pytest
from app.managers.task import TaskManager, get_task_manager
from .mock_repositories import (
    mock_get_task_manager,
    mock_get_task_repository
)


@pytest.mark.asyncio
async def test_get_task_manager(mock_get_task_repository):
    task_manager_generator = get_task_manager(mock_get_task_repository)
    task_manager = await task_manager_generator.__anext__()
    assert isinstance(task_manager, TaskManager)