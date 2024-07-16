from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MarkBase(BaseModel):
    value: int


class MarkCreate(MarkBase):
    student_id: int
    assignment_id: int


class MarkUpdate(MarkBase):
    pass


class Mark(MarkBase):
    id: int
    student_id: int
    assignment_id: int
    date: datetime

    model_config = ConfigDict(from_attributes=True)