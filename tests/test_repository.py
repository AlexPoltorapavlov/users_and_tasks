import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from app.repositories import UserRepository, TaskRepository
from tests.mock_db import session, user_repository, create_users, setup_db, task_repository
from app.schemas.tasks import TaskCreate, TaskRead, TaskUpdate

from app.models import Task

# ***************
# UserRepository Testing
# ***************

@pytest.mark.asyncio
async def test_get_all_empty_database(setup_db, user_repository: UserRepository):
    # Проверка, что метод get_all_users возвращает пустой список, если в базе нет пользователей
    all_users = await user_repository.get_all()
    assert all_users == []

@pytest.mark.asyncio
async def test_get_all(user_repository: UserRepository, create_users):
    # Фикстура setup_db автоматически создаст схему базы данных
    # Фикстура create_users автоматически создаст пользователей
    created_users = create_users  # Получаем список созданных пользователей
    
    # Вызываем метод get_all_users
    all_users = await user_repository.get_all()
    all_users_dicts = [user.__dict__ for user in all_users]

    # Проверки
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
    with pytest.raises(ValueError):
        await task_repository.create_task(task)