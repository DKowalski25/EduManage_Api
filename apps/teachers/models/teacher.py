from sqlalchemy.orm import mapped_column, Mapped, as_declarative, declared_attr, relationship
from sqlalchemy import MetaData, String
from sqlalchemy.sql import func

from datetime import datetime

from apps.students.models.group import Group
from apps.events.models.teacher_class import teacher_class_association_table
from apps.events.models.task import Task

from db import Base


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[int] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    # Connection with the group. Many to many.
    group: Mapped[list[Group]] = relationship(secondary=teacher_class_association_table, back_populates='teacher')
    # Connection with the task. Many to one
    task: Mapped[list[Task]] = relationship(back_populates='teacher')
