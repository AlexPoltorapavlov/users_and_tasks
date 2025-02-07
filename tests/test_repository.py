import pytest
from app.errors import UserNotFoundError
from app.repositories import UserRepository, TaskRepository
from tests.conftest import setup_db
from tests.mock_db import (
        create_users,
        create_tasks,
        user_repository,
        task_repository,
        async_session
    )
from app.schemas.tasks import TaskCreate, TaskUpdate

from app.models import Task

# ***************
# UserRepository Testing
# ***************

@pytest.mark.asyncio
async def test_get_all_empty_database(setup_db, user_repository):
    all_users = await user_repository.get_all()
    print(type(all_users))
    assert all_users == []

@pytest.mark.asyncio
async def test_get_all(user_repository: UserRepository, create_users):
    created_users = create_users

    all_users = await user_repository.get_all()
    all_users_dicts = [user.__dict__ for user in all_users]

    assert len(all_users) == len(created_users)

    for i, user in enumerate(created_users):
        assert all_users_dicts[i]['email'] == user['email']
        assert all_users_dicts[i]['name'] == user['name']

@pytest.mark.asyncio
async def test_get_by_id(user_repository: UserRepository):
    user = await user_repository.get(1)
    print(user.__dict__)

    assert user.email == "user1@example.com"
    assert user.name == "User 1"

@pytest.mark.asyncio
async def test_get_by_id_nonexistent_user(user_repository: UserRepository):
    user = await user_repository.get(999)
    assert user is None

@pytest.mark.asyncio
async def test_get_by_id_invalid_id(user_repository: UserRepository):
    user = await user_repository.get("invalid_id")
    assert user is None


# ***************
# TaskRepository Testing
# ***************

@pytest.mark.asyncio
async def test_get_all_tasks_empty_database(task_repository: TaskRepository):
    all_tasks = await task_repository.get_all_tasks()
    assert all_tasks == []

@pytest.mark.asyncio
async def test_create_task(task_repository: TaskRepository):
    task_data = {"name": "Name", "user_id": 1, "description": "Description", "status": "new"}
    task = TaskCreate(**task_data)
    result = await task_repository.create_task(task)
    assert isinstance(result, Task)
    assert result.name == task_data["name"]
    assert result.user_id == task_data["user_id"]
    assert result.description == task_data["description"]

@pytest.mark.asyncio
async def test_create_task_empty_query(task_repository: TaskRepository):
    task_data = {}
    pytest.raises(ValueError, TaskCreate, **task_data)

@pytest.mark.asyncio
async def test_create_task_nonexistent_user(task_repository: TaskRepository):
    task_data = {"name": "Name", "user_id": 999, "description": "Description", "status": "new"}
    task = TaskCreate(**task_data)
    with pytest.raises(UserNotFoundError):
        await task_repository.create_task(task)

@pytest.mark.asyncio
async def test_get_tasks(task_repository: TaskRepository, create_tasks):
    tasks = await task_repository.get_tasks(1)
    task = tasks[0]
    print(task.__dict__)
    assert len(tasks) == 2
    assert task.name == "Name"
    assert task.user_id == 1
    assert task.description == "Description"
    assert task.status == "new"

    task = tasks[1]
    assert task.name == "Task 1"
    assert task.user_id == 1
    assert task.description == "Description 1"

@pytest.mark.asyncio
async def test_get_tasks_nonexistent_user(task_repository: TaskRepository):
    tasks = await task_repository.get_tasks(999)
    assert tasks == []

@pytest.mark.asyncio
async def test_get_tasks_invalid_id(task_repository: TaskRepository):
    tasks = await task_repository.get_tasks("invalid_id")
    assert tasks == []

@pytest.mark.asyncio
async def test_get_task_by_id(task_repository: TaskRepository):
    task = await task_repository.get_task_by_id(1, 1)
    assert task.name == "Name"
    assert task.user_id == 1
    assert task.description == "Description"
    assert task.status == "new"

@pytest.mark.asyncio
async def test_get_task_by_id_nonexistent_task(task_repository: TaskRepository):
    task = await task_repository.get_task_by_id(999, 1)
    assert task is None

@pytest.mark.asyncio
async def test_get_task_by_id_nonexistent_user(task_repository: TaskRepository):
    task = await task_repository.get_task_by_id(1, 999)
    assert task is None

@pytest.mark.asyncio
async def test_get_task_by_id_invalid_id(task_repository: TaskRepository):
    task = await task_repository.get_task_by_id("invalid_id", 1)
    assert task is None

@pytest.mark.asyncio
async def test_update_task(task_repository: TaskRepository):
    task_data = {"name": "Updated Name", "user_id": 1, "description": "Updated Description", "status": "in_progress"}
    task = TaskUpdate(**task_data)
    result = await task_repository.update_task(1, task, 1)
    assert isinstance(result, Task)
    assert result.name == task_data["name"]
    assert result.user_id == task_data["user_id"]
    assert result.description == task_data["description"]
    assert result.status == task_data["status"]

@pytest.mark.asyncio
async def test_update_task_nonexistent_task(task_repository: TaskRepository):
    task_data = {"name": "Updated Name", "user_id": 1, "description": "Updated Description", "status": "in_progress"}
    task = TaskUpdate(**task_data)
    result = await task_repository.update_task(999, task, 1)
    assert result is None

@pytest.mark.asyncio
async def test_update_task_nonexistent_user(task_repository: TaskRepository):
    task_data = {"name": "Updated Name", "user_id": 1, "description": "Updated Description", "status": "in_progress"}
    task = TaskUpdate(**task_data)
    result = await task_repository.update_task(1, task, 999)
    assert result is None

@pytest.mark.asyncio
async def test_update_task_invalid_id(task_repository: TaskRepository):
    task_data = {"name": "Updated Name", "user_id": 1, "description": "Updated Description", "status": "in_progress"}
    task = TaskUpdate(**task_data)
    result = await task_repository.update_task("invalid_id", task, 1)
    assert result is None

@pytest.mark.asyncio
async def test_delete_task(task_repository: TaskRepository):
    result = await task_repository.delete_task(2, 1)
    assert result.__class__ is Task

@pytest.mark.asyncio
async def test_delete_task_nonexistent_task(task_repository: TaskRepository):
    result = await task_repository.delete_task(999, 1)
    assert result is None

@pytest.mark.asyncio
async def test_delete_task_nonexistent_user(task_repository: TaskRepository):
    result = await task_repository.delete_task(1, 999)
    assert result is None

@pytest.mark.asyncio
async def test_delete_task_invalid_id(task_repository: TaskRepository):
    result = await task_repository.delete_task("invalid_id", 1)
    assert result is None

@pytest.mark.asyncio
async def test_get_all_tasks(task_repository: TaskRepository):
    tasks = await task_repository.get_all_tasks()
    assert len(tasks) == 3

    task = tasks[0]
    assert task.name == "Updated Name"
    assert task.user_id == 1
    assert task.description == "Updated Description"
    assert task.status == "in_progress"

    task = tasks[1]
    assert task.name == "Task 2"
    assert task.user_id == 2
    assert task.description == "Description 2"

    task = tasks[2]
    print(task.id)
    assert task.name == "Task 3"
    assert task.user_id == 3
    assert task.description == "Description 3"

@pytest.mark.asyncio
async def test_get_specific_task_by_id(task_repository: TaskRepository):
    task = await task_repository.get_specific_task_by_id(1)
    assert task.name == "Updated Name"
    assert task.user_id == 1
    assert task.description == "Updated Description"
    assert task.status == "in_progress"

    # Task with id = 2 was deleted in tests before
    task = await task_repository.get_specific_task_by_id(3)
    print(task)
    assert task.name == "Task 2"
    assert task.user_id == 2
    assert task.description == "Description 2"
    assert task.status == "new"

@pytest.mark.asyncio
async def test_get_specific_task_by_id_nonexistent_task(task_repository: TaskRepository):
    task = await task_repository.get_specific_task_by_id(999)
    assert task is None

@pytest.mark.asyncio
async def test_get_specific_task_by_id_invalid_id(task_repository: TaskRepository):
    task = await task_repository.get_specific_task_by_id("invalid_id")
    assert task is None

@pytest.mark.asyncio
async def test_update_specific_task(task_repository: TaskRepository):
    task_data = {"name": "Updated Name", "user_id": 1, "description": "Updated Description", "status": "in_progress"}
    task = TaskUpdate(**task_data)
    result = await task_repository.update_specific_task(1, task)
    assert isinstance(result, Task)
    assert result.name == task_data["name"]
    assert result.user_id == task_data["user_id"]
    assert result.description == task_data["description"]
    assert result.status == task_data["status"]

@pytest.mark.asyncio
async def test_update_specific_task_nonexistent_task(task_repository: TaskRepository):
    task_data = {"name": "Updated Name", "user_id": 1, "description": "Updated Description", "status": "in_progress"}
    task = TaskUpdate(**task_data)
    result = await task_repository.update_specific_task(999, task)
    assert result is None

@pytest.mark.asyncio
async def test_update_specific_task_invalid_id(task_repository: TaskRepository):
    task_data = {"name": "Updated Name", "user_id": 1, "description": "Updated Description", "status": "in_progress"}
    task = TaskUpdate(**task_data)
    result = await task_repository.update_specific_task("invalid_id", task)
    assert result is None

@pytest.mark.asyncio
async def test_delete_specific_task(task_repository: TaskRepository):
    result = await task_repository.delete_specific_task(1)
    assert result.__class__ is Task

@pytest.mark.asyncio
async def test_delete_specific_task_nonexistent_task(task_repository: TaskRepository):
    result = await task_repository.delete_specific_task(999)
    assert result is None

@pytest.mark.asyncio
async def test_delete_specific_task_invalid_id(task_repository: TaskRepository):
    result = await task_repository.delete_specific_task("invalid_id")
    assert result is None