from pydantic import BaseModel, EmailStr


class SignUp(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str
    password: str
