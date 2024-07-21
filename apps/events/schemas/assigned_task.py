from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class AssignedTaskBase(BaseModel):
    assigned_at: datetime


class AssignedTaskCreate(AssignedTaskBase):
    assignment_id: int
    group_id: Optional[int]
    student_id: Optional[int]


class AssignedTaskUpdate(AssignedTaskBase):
    pass


class AssignedTask(AssignedTaskBase):
    id: int
    assignment_id: int
    group_id: int | None
    student_id: int | None

    class Config:
        from_attributes = True
