from app.repositories import TaskRepository
from app.db import get_task_db
from fastapi import Depends
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskRead

class TaskManager:
    def __init__(self, task_db):
        self.task_db = task_db

async def create_task(self, task_data: TaskCreate):
    result = await self.task_db.create_task(task_data)
    return TaskRead(**result.__dict__) if result else None

async def get_tasks(self, user_id: int):
    results = await self.task_db.get_tasks(user_id)
    return [TaskRead(**task.__dict__) for task in results] if results else []

async def get_all_tasks(self):
    results = await self.task_db.get_all_tasks()
    return [TaskRead(**task.__dict__) for task in results] if results else []

async def get_task_by_id(self, task_id: int, user_id: int):
    result = await self.task_db.get_task_by_id(task_id, user_id)
    return TaskRead(**result.__dict__) if result else None

async def get_specific_task_by_id(self, task_id: int):
    result = await self.task_db.get_specific_task_by_id(task_id)
    return TaskRead(**result.__dict__) if result else None

async def update_task(self, task_id: int, task_data: TaskUpdate, user_id: int):
    result = await self.task_db.update_task(task_id, task_data, user_id)
    return TaskRead(**result.__dict__) if result else None

async def update_specific_task(self, task_id: int, task_data: TaskUpdate):
    result = await self.task_db.update_specific_task(task_id, task_data)
    return TaskRead(**result.__dict__) if result else None

async def delete_specific_task(self, task_id: int):
    result = await self.task_db.delete_specific_task(task_id)
    return TaskRead(**result.__dict__) if result else None


async def get_task_manager(task_db: TaskRepository = Depends(get_task_db)):
    if not isinstance(task_db, TaskRepository):
        raise TypeError(f"Expected TaskRepository, got {type(task_db).__name__}")
    yield TaskManager(task_db)