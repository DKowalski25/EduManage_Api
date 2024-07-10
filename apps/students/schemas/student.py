from pydantic import BaseModel, EmailStr, ConfigDict


class Student(BaseModel):
    id: int
    h: str
    last_name: str
    email: EmailStr
    phone_number: int
    grade: int
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
