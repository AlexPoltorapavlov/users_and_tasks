from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTable, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
 