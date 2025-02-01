import pytest
from pytest_asyncio import fixture as async_fixture
from fastapi.testclient import TestClient
from app.main import app
from pytest import fixture
from tests.test_database import (
    get_client,
    token,
    make_test_user,
    get_test_user,
    setup_db
)

@pytest.mark.asyncio
async def test_setup_db(setup_db, make_test_user):
    pass

@pytest.mark.asyncio
async def test_create_task_unauthorized(get_client):
    client = get_client
    task_data = {
        "name": "Test Task",
        "description": "Test Description",
        "status": "new"
    }

    response = client.post(
        "/tasks",
        json=task_data
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_task(get_client, token):
    client = get_client
    task_data = {
        "name": "Test Task",
        "description": "Test Description",
        "status": "new"
    }

    response = client.post(
        "/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test Task"
    assert response.json()["description"] == "Test Description"

@pytest.mark.asyncio
async def test_create_task_invalid_data(get_client, token):
    client = get_client

    task_data = {
        "name": "Test Task",
        "description": "Test Description",
        "status": "invalid_status"
    }

    response = client.post(
        "/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_task_missing_status(get_client, token):
    client = get_client

    task_data = {
        "name": "Test Task",
        "description": "Test Description",
        # status: Optional[enum] = "new"
    }

    response = client.post(
        "/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "new"

@pytest.mark.asyncio
async def test_create_task_missing_description_or_name(get_client, token):
    client = get_client

    task_data = {
        "name": "Test Task",
        # description: str 
        "status": "new"
    }

    response = client.post(
        "/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    task_data = {
        # name: str
        "description": "Test Description",
        "status": "new"
    }

    response = client.post(
        "/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_all_tasks(get_client, token):
    client = get_client

    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_all_tasks_unauthorized(get_client):
    client = get_client

    response = client.get(
        "/tasks"
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_task(get_client, token):
    client = get_client

    response = client.get(
        "/tasks/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.asyncio
async def test_get_task_unauthorized(get_client):
    client = get_client

    response = client.get(
        "/tasks/1"
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_task_wrond_id(get_client, token):
    client = get_client

    response = client.get(
        "/tasks/-1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == None

@pytest.mark.asyncio
async def test_get_task_invalid_id(get_client, token):
    client = get_client

    response = client.get(
        "/tasks/invalid_id",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_update_task(get_client, token):
    client = get_client

    task_data = {
        "name": "Updated Task",
        "description": "Updated Description",
        "status": "in_progress"
    }

    response = client.put(
        "/tasks/1",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Task"
    assert response.json()["description"] == "Updated Description"
    assert response.json()["status"] == "in_progress"

@pytest.mark.asyncio
async def test_update_task_unauthorized(get_client):
    client = get_client

    task_data = {
        "name": "Updated Task",
        "description": "Updated Description",
        "status": "in_progress"
    }

    response = client.put(
        "/tasks/1",
        json=task_data
    )

    assert response.status_code == 401