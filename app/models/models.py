from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeBase, validates, relationship
from sqlalchemy import Column, String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    tasks = relationship('Task', back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', back_populates="tasks")

    @validates('status')
    def validate_fields(self, key, value):
        if key == 'status' and value not in ['new', 'in_progress', 'completed']:
            raise ValueError('Invalid status')

        return value
