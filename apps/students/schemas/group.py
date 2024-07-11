from pydantic import BaseModel, ConfigDict


class Student(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class AssignedTask(BaseModel):
    id: int
    task_id: int

    class Config:
        orm_mode = True


class FullGroup(BaseModel):
    id: int
    group_name: str
    students: list[Student] = []
    assigned_tasks: list[AssignedTask] = []

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class Group(BaseModel):
    id: int
    group_name: str

    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True

