import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from collections.abc import AsyncGenerator
from app.models.models import Base
import os
from app.dal.task import TaskRepository
import app.schemas.tasks as TaskScheme
from app.models.models import Task

@pytest.fixture(scope="session")
def db_file():
    db_path = "test_database.db"
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest_asyncio.fixture(scope="session")
async def engine(db_file):
    DATABASE_URL = f"sqlite+aiosqlite:///{db_file}"
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def create_db_and_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@pytest_asyncio.fixture(scope="session")
async def async_session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture()
async def session(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@pytest_asyncio.fixture()
async def test_db(create_db_and_tables, session):
    return session

# The tests
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