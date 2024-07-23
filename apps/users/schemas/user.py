from pydantic import BaseModel, EmailStr

from datetime import datetime


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True
