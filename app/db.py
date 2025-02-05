from collections.abc import AsyncGenerator
from .config import config

from fastapi import Depends
from app.repositories import UserRepository, TaskRepository
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import Task, User
from app.models.base_model import Base


DATABASE_URL = config.DATABASE_URL


engine = create_async_engine(DATABASE_URL)
Base.metadata.bind = engine
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    """Create all database tables defined in the metadata.

    This function is used to initialize the database schema by creating all tables
    defined in the SQLAlchemy `Base.metadata`.

    Note:
        This should typically be called once during application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency function to provide an async database session.

    Yields:
        AsyncSession: An async SQLAlchemy session for database operations.

    Note:
        This function is used as a dependency in FastAPI routes to inject a database session.
    """
    async with async_session_maker() as session:
        yield session

