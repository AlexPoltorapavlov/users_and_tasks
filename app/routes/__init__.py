from app.routes.authenticated import router as authenticated_router
from app.routes.tasks import router as tasks_router
from app.routes.users import router as users_router

__all__ = ["authenticated_router",
           "tasks_router",
           "users_router"]