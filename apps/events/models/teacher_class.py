from sqlalchemy import Table, Column, ForeignKey

from db import Base

teacher_class_association_table = Table(
    "teacher_class_association_table",
    Base.metadata,
    Column('teacher_id', ForeignKey("users.id"), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True)
)