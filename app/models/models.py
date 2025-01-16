from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeBase, validates, relationship
from sqlalchemy import Column, String, Integer, ForeignKey

class Base(DeclarativeBase):
    pass

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

class Task(Base):
    """Task model representing a task in the database."""

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    """Primary key for the task, auto-incremented."""

    name = Column(String)
    """Name of the task."""

    description = Column(String)
    """Description of the task."""

    status = Column(String, nullable=False, default='new')
    """Status of the task. Defaults to 'new' and must be one of ['new', 'in_progress', 'completed']."""

    user_id = Column(Integer, ForeignKey(User.id))
    """Foreign key referencing the user who owns the task."""

    user = relationship('User', back_populates="tasks")
    """Relationship to the User model, establishing the many-to-one relationship between Task and User."""

    @validates('status')
    def validate_fields(self, key, value):
        """Validates the 'status' field to ensure it has a valid value.

        Args:
            key (str): The name of the field being validated.
            value (str): The value being assigned to the field.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If the value is not one of ['new', 'in_progress', 'completed'].
        """
        if key == 'status' and value not in ['new', 'in_progress', 'completed']:
            raise ValueError('Invalid status')

        return value
