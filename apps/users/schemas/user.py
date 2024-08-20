from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCreate(User):
    password: str


class UserUpdate(User):
    pass


class FullUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str
    hashed_password: str

    model_config = ConfigDict(
        from_attributes=True,
    )
