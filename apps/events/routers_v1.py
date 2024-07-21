from .mark_router import router as mark_roure
from .assignment_router import router as assignment_roure

routers = (
    {"router": mark_roure, "extra_params": {"tags": ("marks", )}},
    {"router": assignment_roure, "extra_params": {"tags": ("assignments", )}},
)

__all__ = (
    'routers',
)
