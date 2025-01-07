from typing import Optional
from pydantic import BaseModel, field_validator

class TaskBaseModel(BaseModel):
    @field_validator('status')
    def validators(self, key, value):
        if key == 'status' and value not in ['new', 'in_progress', 'completed']:
            raise ValueError('Invalid status')
        return value


class TaskRead(TaskBaseModel):
    id: int
    name: str
    description: str
    status: str
    user_id: int

class TaskCreate(TaskBaseModel):
    name: str
    description: str
    status: str = 'new'
    user_id: int

class TaskUpdate(TaskBaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
