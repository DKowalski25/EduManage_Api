from pydantic import BaseModel, EmailStr

from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    role: str


class UserCreate(UserBase):
    password: str
    group_id: int


class UserUpdate(UserBase):
    group_id: int


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    classes: list[int] | None  # List of class IDs (for teachers).
    assignments: list[int] | None  # List of assignment IDs.
    assigned_tasks: list[int] | None  # List of assigned task IDs.
    marks: list[int] | None  # List of mark IDs.

    class Config:
        orm_mode = True
