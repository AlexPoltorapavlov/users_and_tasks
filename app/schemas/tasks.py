from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator

class StatusEnum(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    completed = 'completed'

class TaskRead(BaseModel):
    id: int
    name: str
    description: str
    status: StatusEnum
    user_id: int

class TaskCreate(BaseModel):
    name: str
    description: str
    status: Optional[StatusEnum] = StatusEnum.new

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None

