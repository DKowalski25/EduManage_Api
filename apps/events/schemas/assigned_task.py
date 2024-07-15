from pydantic import BaseModel
from datetime import datetime


class AssignedTaskBase(BaseModel):
    assigned_at: datetime


class AssignedTaskCreate(AssignedTaskBase):
    assignment_id: int
    group_id: int | None
    student_id: int | None


class AssignedTaskUpdate(AssignedTaskBase):
    pass


class AssignedTask(AssignedTaskBase):
    id: int
    assignment_id: int
    group_id: int | None
    student_id: int | None

    class Config:
        orm_mode = True
