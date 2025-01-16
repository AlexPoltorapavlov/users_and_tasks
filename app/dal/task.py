from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.models import Task
from ..schemas.tasks import *
from ..db import get_async_session

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_data: TaskCreate, user_id: int):
        task = Task(**task_data.model_dump(), user_id = user_id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_tasks(self, user_id: int):
        result = await self.session.execute(select(Task).where(Task.user_id == user_id))
        return result.scalars().all()

    async def get_task_by_id(self, task_id: int, user_id: int):
        result = await self.session.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
        task = result.scalar_one_or_none()
        return task if task else None

    async def update_task(self, task_id: int, task_data: TaskUpdate, user_id: int):
        task = await self.get_task_by_id(task_id, user_id)
        if task is None:
            return None

        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id: int, user_id: int):
        task = await self.get_task_by_id(task_id, user_id)
        if task is None:
            return None
        
        await self.session.delete(task)
        await self.session.commit()
        return task


async def get_task_db(session: AsyncSession = Depends(get_async_session)):
    yield TaskRepository(session)