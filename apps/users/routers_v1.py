from .user_router import router as user_router

routers = ({"router": user_router, "extra_params": {"tags": ("users", )}}, )

__all__ = (
    'routers',
)
