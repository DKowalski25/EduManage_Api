from .mark_router import router as mark_roure

routers = ({"router": mark_roure, "extra_params": {"tags": ("marks", )}}, )

__all__ = (
    'routers',
)
