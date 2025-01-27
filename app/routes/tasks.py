from fastapi import APIRouter, Depends
from app.schemas import TaskRead, TaskCreate, TaskUpdate, UserRead
from app.managers import get_task_manager
from ..auth.auth import current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

def check_is_admin(user: UserRead = Depends(current_active_user)):
    """Check if the user is an admin.

    Args:
        user (UserRead): The authenticated user.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    return user.is_superuser

@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate,
                      user: UserRead = Depends(current_active_user),
                      is_admin: bool = Depends(check_is_admin),
                      task_manager = Depends(get_task_manager)):

    if is_admin and task.user_id is not None:
        return await task_manager.create_task(task_data=task)
    else:
        task.user_id = user.id
    return await task_manager.create_task(task_data=task)

@router.get("/")
async def get_all_tasks(user: UserRead = Depends(current_active_user),
                        is_admin: bool = Depends(check_is_admin),
                        task_manager = Depends(get_task_manager)):
    if is_admin:
        return await task_manager.get_all_tasks()
    else:
        return await task_manager.get_tasks(user.id)

@router.get("/{task_id}")
async def get_task(task_id: int,
                   user: UserRead = Depends(current_active_user),
                   is_admin: bool = Depends(check_is_admin),
                   task_manager = Depends(get_task_manager)):

    if is_admin:
        return await task_manager.get_specific_task_by_id(task_id)
    else:
        return await task_manager.get_task_by_id(task_id, user.id)

@router.put("/{task_id}")
async def update_task(task_id: int,
                      task_data: TaskUpdate,
                      user: UserRead = Depends(current_active_user),
                      task_manager = Depends(get_task_manager),
                      is_admin: bool = Depends(check_is_admin)):

    if is_admin:
        return await task_manager.update_specific_task(task_id, task_data)
    else:
        return await task_manager.update_task(task_id, task_data, user.id)

@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      user: UserRead = Depends(current_active_user),
                      task_manager = Depends(get_task_manager),
                      is_admin: bool = Depends(check_is_admin)):

    if is_admin:
        return await task_manager.delete_specific_task(task_id)
    else:
        return await task_manager.delete_task(task_id, user.id)

