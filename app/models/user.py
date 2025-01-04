from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from app.db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    username: str
    password: str