from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date


class AssignedTasks(BaseModel):
    id: int
    assignment_id: int | None
    student_id: int | None
    group_id: int | None

    class Config:
        orm_mode = True


class Group(BaseModel):
    id: int
    group_name: str
    grade: int

    class Config:
        orm_mode = True


class FullStudent(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int | None
    grade: int
    group_id: int | None
    created_at: date | None
    hashed_password: str
    group: Group | None
    assigned_tasks: list[AssignedTasks] = []

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class Student(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    grade: int
    group_id: int | None

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True
