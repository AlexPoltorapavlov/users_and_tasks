from pytest_asyncio import fixture as async_fixture
from app.repositories import TaskRepository
from unittest.mock import AsyncMock

@async_fixture
async def get_task_manager():
    session = AsyncMock()
    yield TaskRepository(session)