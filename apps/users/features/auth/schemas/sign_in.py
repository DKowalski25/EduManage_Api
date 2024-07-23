from pydantic import BaseModel, EmailStr


class SignIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
