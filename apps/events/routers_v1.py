from .mark_router import router as mark_roure
from .assignment_router import router as assignment_roure
from .assigned_task_router import router as assigned_task_roure

routers = (
    {"router": mark_roure, "extra_params": {"tags": ("marks", )}},
    {"router": assignment_roure, "extra_params": {"tags": ("assignments", )}},
    {"router": assigned_task_roure, "extra_params": {"tags": ("assigned_tasks", )}}
)

__all__ = (
    'routers',
)
