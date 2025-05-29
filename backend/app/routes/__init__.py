# app/routes/__init__.py

from .users import router as users_router
from .projects import router as projects_router
from .tasks import router as tasks_router
from .categories import router as categories_router

__all__ = ["users_router", "projects_router", "tasks_router", "categories_router"]
