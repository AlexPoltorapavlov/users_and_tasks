from fastapi import APIRouter, Depends
from app.schemas import TaskRead, TaskCreate, TaskUpdate, UserRead
from app.managers import get_task_manager
from ..auth.auth import current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

def check_is_admin(user: UserRead = Depends(current_active_user)):
    """
    Dependency function to check if the current user has admin privileges.

    Args:
        user (UserRead): Current authenticated user, injected by FastAPI

    Returns:
        bool: True if user is an admin, False otherwise
    """
    return user.is_superuser

@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate,
                      user: UserRead = Depends(current_active_user),
                      is_admin: bool = Depends(check_is_admin),
                      task_manager = Depends(get_task_manager)):
    """
    Create a new task.

    Allows regular users to create tasks for themselves and admins to create tasks
    for any user.

    Args:
        task (TaskCreate): Task data to create
        user (UserRead): Current authenticated user
        is_admin (bool): Whether the current user is an admin
        task_manager: Task manager instance for handling task operations

    Returns:
        TaskRead: Created task data

    Notes:
        - Regular users can only create tasks for themselves
        - Admins can create tasks for any user by specifying user_id
    """
    if is_admin and task.user_id is not None:
        return await task_manager.create_task(task_data=task)
    else:
        task.user_id = user.id
    return await task_manager.create_task(task_data=task)

@router.get("/")
async def get_all_tasks(user: UserRead = Depends(current_active_user),
                        is_admin: bool = Depends(check_is_admin),
                        task_manager = Depends(get_task_manager)):
    """
    Retrieve all tasks.

    Returns all tasks for admins, or only the user's tasks for regular users.

    Args:
        user (UserRead): Current authenticated user
        is_admin (bool): Whether the current user is an admin
        task_manager: Task manager instance for handling task operations

    Returns:
        list[TaskRead]: List of tasks
        
    Notes:
        - Regular users can only see their own tasks
        - Admins can see all tasks in the system
    """
    if is_admin:
        return await task_manager.get_all_tasks()
    else:
        return await task_manager.get_tasks(user.id)

@router.get("/{task_id}")
async def get_task(task_id: int,
                   user: UserRead = Depends(current_active_user),
                   is_admin: bool = Depends(check_is_admin),
                   task_manager = Depends(get_task_manager)):
    """
    Retrieve a specific task by ID.

    Args:
        task_id (int): ID of the task to retrieve
        user (UserRead): Current authenticated user
        is_admin (bool): Whether the current user is an admin
        task_manager: Task manager instance for handling task operations

    Returns:
        TaskRead: Task data if found

    Notes:
        - Regular users can only retrieve their own tasks
        - Admins can retrieve any task
    """
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
    """
    Update a specific task.

    Args:
        task_id (int): ID of the task to update
        task_data (TaskUpdate): Updated task data
        user (UserRead): Current authenticated user
        task_manager: Task manager instance for handling task operations
        is_admin (bool): Whether the current user is an admin

    Returns:
        TaskRead: Updated task data

    Notes:
        - Regular users can only update their own tasks
        - Admins can update any task
    """
    if is_admin:
        return await task_manager.update_specific_task(task_id, task_data)
    else:
        return await task_manager.update_task(task_id, task_data, user.id)

@router.delete("/{task_id}")
async def delete_task(task_id: int,
                      user: UserRead = Depends(current_active_user),
                      task_manager = Depends(get_task_manager),
                      is_admin: bool = Depends(check_is_admin)):
    """
    Delete a specific task.

    Args:
        task_id (int): ID of the task to delete
        user (UserRead): Current authenticated user
        task_manager: Task manager instance for handling task operations
        is_admin (bool): Whether the current user is an admin

    Returns:
        TaskRead: Deleted task data

    Notes:
        - Regular users can only delete their own tasks
        - Admins can delete any task
    """
    if is_admin:
        return await task_manager.delete_specific_task(task_id)
    else:
        return await task_manager.delete_task(task_id, user.id)

