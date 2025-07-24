from .books import router as books_router
from .categories import router as categories_router
from .health import router as health_router
from .stats import router as stats_router

__all__ = ["books_router", "categories_router", "stats_router", "health_router"]
