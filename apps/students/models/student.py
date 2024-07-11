from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.sql import func

from datetime import datetime

from apps.events.models.task import Task
from apps.events.models.assigned_tasks import assigned_task_association_table

from group import Group
from db import Base


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(12))
    grade: Mapped[int]
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    # Connection to group. One to many.
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped[Group] = relationship(back_populates="student")
    # Connection with the task. Many to many
    task: Mapped[list[Task]] = relationship(secondary=assigned_task_association_table, back_populates='student')
