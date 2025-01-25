from collections.abc import AsyncGenerator
import os
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.models import Base
from app.dal.user import UserRepository
from app.models.models import User
from pytest_asyncio import fixture as async_fixture

# адрес к тестовой базе данных
TEST_DATABASE_URL = "sqlite+aiosqlite:///test_db.db"

# создание движка. Включает в себя адрес бд
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)

@async_fixture(scope="session")
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    if os.path.exists("test_db.db"):
        os.remove("test_db.db")

@async_fixture
async def session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


@async_fixture
async def user_repository(session: AsyncSession) -> UserRepository:
    return UserRepository(session, User)


# usefull fixtures
@async_fixture
async def create_users(user_repository: UserRepository):
    users_dict = [
        {'email': 'user1@example.com', 'hashed_password': 'password1', 'name': 'User 1'},
        {'email': 'user2@example.com', 'hashed_password': 'password2', 'name': 'User 2'},
        {'email': 'user3@example.com', 'hashed_password': 'password3', 'name': 'User 3'},
    ]

    for user in users_dict:
        await user_repository.create(user)

    return users_dict