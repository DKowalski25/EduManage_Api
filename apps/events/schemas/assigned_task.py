from pydantic import BaseModel, ConfigDict
from datetime import date


class FullAssignedTasks(BaseModel):
    id: int
    assignment_id: int
    group_id: int | None = None
    student_id: int | None = None
    assigned_at: date

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class AssignedTasks(BaseModel):
    id: int
    assignment_id: int
    assigned_at: date

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True
