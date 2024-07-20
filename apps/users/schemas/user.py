from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    # classes: list[int] | None  # List of class IDs (for teachers).
    # assignments: list[int] | None  # List of assignment IDs.
    # assigned_tasks: list[int] | None  # List of assigned task IDs.
    # marks: list[int] | None  # List of mark IDs.

    model_config = ConfigDict(from_attributes=True)
