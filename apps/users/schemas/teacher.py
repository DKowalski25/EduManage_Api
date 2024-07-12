from pydantic import BaseModel, EmailStr, ConfigDict


class TeacherClass(BaseModel):
    group_id: int

    class Config:
        orm_mode = True


class Task(BaseModel):
    id: int
    title: str
    due_date: str

    class Config:
        orm_mode = True


class FullTeacher(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    hashed_password: str
    teacher_classes: list[TeacherClass] = []
    tasks: list[Task] = []

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class Teacher(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True

