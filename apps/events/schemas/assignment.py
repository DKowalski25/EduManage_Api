from pydantic import BaseModel, ConfigDict

from datetime import datetime


class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: datetime


class AssignmentCreate(AssignmentBase):
    teacher_id: int


class AssignmentUpdate(AssignmentBase):
    pass


class Assignment(AssignmentBase):
    id: int
    created_at = datetime
    teacher_id: int
    assigned_tasks: list[int] | None  # List of assigned task IDs.

    model_config = ConfigDict(from_attributes=True)
