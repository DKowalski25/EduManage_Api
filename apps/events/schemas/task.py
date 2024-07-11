from pydantic import BaseModel, ConfigDict
from datetime import date


class AssignedTasks(BaseModel):
    id: int
    student_id: int | None
    group_id: int | None

    class Config:
        orm_mode = True


class Teacher(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class FullAssignment(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: date
    due_date: date
    teacher: Teacher
    assigned_tasks: list[AssignedTasks] = []

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class Assignment(BaseModel):
    id: int
    title: str
    due_date: date
    teacher_id: int

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True
