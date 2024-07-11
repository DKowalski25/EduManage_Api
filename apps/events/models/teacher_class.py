from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Table, Column, ForeignKey

from db import Base


teacher_class_association_table = Table(
    "teacher_class_association_table",
    Base.metadata,
    Column('teacher_id', ForeignKey("teachers.id"), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True)
)


