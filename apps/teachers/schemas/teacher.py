from pydantic import BaseModel, EmailStr, ConfigDict


class Teacher(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
