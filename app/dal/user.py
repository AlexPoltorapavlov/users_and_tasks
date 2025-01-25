from fastapi_users.db import SQLAlchemyUserDatabase
from app.models.models import User
from sqlalchemy import select

class UserRepository(SQLAlchemyUserDatabase):
    """Repository class for handling user-related database operations.

    This class extends SQLAlchemyUserDatabase to provide additional functionality
    for user management in the database.

    Attributes:
        session: SQLAlchemy async session object for database operations.
    """

    async def get_all(self):
        """Retrieves all users from the database.

        Returns:
            list[User]: A list of all User objects in the database.

        Example:
            >>> repo = UserRepository(session)
            >>> users = await repo.get_all()
        """
        async with self.session as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users