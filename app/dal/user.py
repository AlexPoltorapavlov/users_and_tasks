from fastapi_users.db import SQLAlchemyUserDatabase
from app.models.models import User
from sqlalchemy import select

class UserRepository(SQLAlchemyUserDatabase):
    async def get_all(self):
        async with self.session as session:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return users