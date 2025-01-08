from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.models import Task

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_data, user_id: int):
        task = Task(**task_data.dict(), user_id = user_id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_tasks(self, user_id: int):
        result = await self.session.execute(select(Task).where(Task.user_id == user_id))
        return result.scalar().all()

    async def get_task_by_id(self, task_id: int, user_id: int):
        result = await self.session.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
        return result.scalar_one_or_none()

    async def update_task(self, task_id: int, task_data, user_id: int):
        task = self.get_task_by_id(task_id, user_id)
        if task is None:
            return None

        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)

        self.session.commit()
        self.session.refresh(task)
        return task

    async def delete_task(self, task_id: int, user_id: int):
        task = self.get_task_by_id(task_id, user_id)
        if task is None:
            return None
        
        self.session.delete(task)
        self.session.commit()
        return task
