from fastapi import APIRouter, Depends
from app.auth.auth import current_active_user
from app.models import User

router = APIRouter()

@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    """Endpoint to demonstrate authentication.

    This route is protected and requires the user to be authenticated. It returns a message
    confirming authentication along with the authenticated user's ID.

    Args:
        user (User): The authenticated user, automatically injected by the `current_active_user` dependency.

    Returns:
        dict: A dictionary containing a confirmation message and the authenticated user's ID.
    """
    return {"message": "You are authenticated", "user_id": user.id}