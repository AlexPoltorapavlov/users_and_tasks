import pytest
from pytest_asyncio import fixture as async_fixture
from fastapi.testclient import TestClient
from app.main import app
from pytest import fixture
from tests.test_database import (
    get_client,
    token,
    get_test_user,
    setup_db
)

@pytest.mark.asyncio
async def test_setup_db(setup_db):
    pass

""" @async_fixture(scope="module")
async def get_client():
    client = TestClient(app)
    yield client

@fixture(scope="module")
def make_user(get_client):
    client = get_client
    user_data = {"email": "user@example.com", "password": "string", "name": "string"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    return user_data

@fixture(scope="function")
def get_access_token(get_client):
    client = get_client
    user_data = {"email": "user@example.com", "password": "string", "name": "string"}
    response = client.post("/auth/jwt/login", data={"username": user_data["email"], "password": user_data["password"]})
    assert response.status_code == 200
    return response.json()["access_token"] """

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