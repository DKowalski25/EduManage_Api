from pydantic import BaseModel, EmailStr

from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    classes: list[int] | None  # List of class IDs (for teachers).
    assignments: list[int] | None  # List of assignment IDs.
    assigned_tasks: list[int] | None  # List of assigned task IDs.
    marks: list[int] | None  # List of mark IDs.

    # model_config = ConfigDict(from_attributes=True)

    class Config:
        from_attributes = True
