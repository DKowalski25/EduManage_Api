from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.sql import func

from datetime import datetime

from apps.students.models.student import Student
from apps.students.models.group import Group

from assigned_tasks import assigned_task_association_table

from db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    due_date: Mapped[datetime]

    # Connection with the teacher. One to many.
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    teacher: Mapped[str] = relationship(back_populates='task')
    # Connection with the student. Many to many.
    student: Mapped[list[Student]] = relationship(secondary=assigned_task_association_table, back_populates='task')
    # Connection with group. Many to many.
    group: Mapped[list[Group]] = relationship(secondary=assigned_task_association_table, back_populates='task')
