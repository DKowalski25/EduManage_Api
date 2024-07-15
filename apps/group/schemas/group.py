from pydantic import BaseModel

from datetime import datetime


class GroupBase(BaseModel):
    group_name: str
    description: str
    grade: int


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    created_at: datetime
    updated_at: datetime
    teachers: list[int] | None  # List of teacher IDs.
    students: list[int] | None  # List of student IDs.
    assigned_tasks: list[int] | None  # List of assigned task IDs.

    class Config:
        orm_mode = True
