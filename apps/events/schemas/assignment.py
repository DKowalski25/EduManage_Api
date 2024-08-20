from enum import Enum

from pydantic import BaseModel, ConfigDict

from datetime import datetime


class AssignmentType(str, Enum):
    EXAM = "exam"
    CREDIT = "credit"
    HOMEWORK = "homework"


class AssignmentBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    type: AssignmentType


class AssignmentCreate(AssignmentBase):
    teacher_id: int


class AssignmentUpdate(AssignmentBase):
    pass


class Assignment(AssignmentBase):
    id: int
    created_at: datetime
    teacher_id: int
    assigned_tasks: list[int] | None  # List of assigned task IDs.

    model_config = ConfigDict(
        from_attributes=True,
    )
