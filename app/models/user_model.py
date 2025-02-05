from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey
from app.models.base_model import Base

class User(SQLAlchemyBaseUserTable, Base):
    """User model representing a user in the database.

    Inherits from SQLAlchemyBaseUserTable to include default fields required by FastAPI Users.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    """Primary key for the user, auto-incremented."""

    name = Column(String, nullable=True)
    """Name of the user. Optional field."""

    tasks = relationship('Task', back_populates="user")
    """Relationship to the Task model, establishing a one-to-many relationship between User and Task."""