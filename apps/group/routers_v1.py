from .group_router import router as group_router

routers = ({"router": group_router, "extra_params": {"tags": ("groups", )}}, )

__all__ = (
    'routers',
)
