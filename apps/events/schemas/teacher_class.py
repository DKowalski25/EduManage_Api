from pydantic import BaseModel, ConfigDict


class FullTeacherClass(BaseModel):
    teacher_id: int
    group_id: int

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class TeacherClass(BaseModel):
    teacher_id: int
    group_id: int

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True
