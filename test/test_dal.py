import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from collections.abc import AsyncGenerator
from app.models.models import Base
import os

@pytest.fixture(scope="session")
def db_file():
    db_path = "test_database.db"
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture(scope="session")
async def engine(db_file):
    DATABASE_URL = f"sqlite+aiosqlite:///{db_file}"
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="session")
async def create_db_and_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session")
async def async_session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)

@pytest.fixture()
async def session(async_session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@pytest.fixture()
async def test_db(create_db_and_tables, session):
    return session
