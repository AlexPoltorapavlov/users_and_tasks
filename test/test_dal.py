import pytest
import pytest_asyncio
from sqlalchemy import select
from app.dal.task import TaskRepository
import app.schemas.tasks as TaskScheme
from app.models.models import Task
from .conftest import test_db

@pytest.mark.asyncio
async def test_create_task(test_db):
    repo = TaskRepository(test_db)

    task_data = TaskScheme.TaskCreate(name="Test Task", description="This is a test task")
    user_id = 1

    created_task = await repo.create_task(task_data=task_data, user_id=user_id)

    assert created_task.id is not None
    assert created_task.name == task_data.name
    assert created_task.description == task_data.description
    assert created_task.user_id == user_id

    retrieved_task = await test_db.get(Task, created_task.id)
    assert retrieved_task is not None
    assert retrieved_task.name == task_data.name
    assert retrieved_task.description == task_data.description
    assert retrieved_task.user_id == user_id

@pytest.mark.asyncio
async def test_get_tasks(test_db):
    repo = TaskRepository(test_db)
    user_id = 1
    tasks = await repo.get_tasks(user_id=user_id)

    assert tasks is not None
    assert len(tasks) == 1

@pytest.mark.asyncio
async def test_get_task_by_id(test_db):
    repo = TaskRepository(test_db)
    user_id, task_id = 1, 1
    retrieved_task = await repo.get_task_by_id(task_id, user_id)
    task_data = TaskScheme.TaskCreate(name="Test Task", description="This is a test task")

    assert retrieved_task is not None
    assert retrieved_task.name == task_data.name
    assert retrieved_task.description == task_data.description
    assert retrieved_task.user_id == user_id


@pytest.mark.asyncio
async def test_update_task(test_db):
    repo = TaskRepository(test_db)
    user_id, task_id = 1, 1
    task_data = TaskScheme.TaskCreate(name="Task for tests", description="This is THE test task", status="in_progress")
    updated_task = await repo.update_task(task_id, task_data, user_id)

    assert updated_task is not None
    assert updated_task.name == task_data.name
    assert updated_task.description == task_data.description
    assert updated_task.user_id == user_id

    retrieved_task = await test_db.get(Task, updated_task.id)
    assert retrieved_task is not None
    assert retrieved_task.name == task_data.name
    assert retrieved_task.description == task_data.description
    assert retrieved_task.user_id == user_id

@pytest.mark.asyncio
async def test_delete_task(test_db):
    repo = TaskRepository(test_db)
    user_id, task_id = 1, 1

    deleted_task = await repo.delete_task(task_id, user_id)
    query = select(Task)
    result = await test_db.execute(query)
    tasks = result.scalars().all()

    assert len(tasks) == 0
    assert deleted_task.id == 1

