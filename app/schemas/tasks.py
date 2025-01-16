from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator

class StatusEnum(str, Enum):
    """Enum representing the possible statuses of a task."""

    new = "new"
    """Task is newly created and not yet started."""
    in_progress = "in_progress"
    """Task is currently in progress."""
    completed = "completed"
    """Task has been completed."""

class TaskRead(BaseModel):
    """Schema for reading task data."""

    id: int
    """The unique identifier of the task."""
    name: str
    """The name of the task."""
    description: str
    """The description of the task."""
    status: StatusEnum
    """The current status of the task."""
    user_id: int
    """The ID of the user associated with the task."""

class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    name: str
    """The name of the task."""
    description: str
    """The description of the task."""
    status: Optional[StatusEnum] = StatusEnum.new
    """The status of the task. Defaults to 'new' if not provided."""


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    name: Optional[str] = None
    """The updated name of the task. Optional."""
    description: Optional[str] = None
    """The updated description of the task. Optional."""
    status: Optional[StatusEnum] = None
    """The updated status of the task. Optional."""