from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from apps.teachers.models.teacher import Teacher
from apps.events.models.teacher_class import teacher_class_association_table

from student import Student
from db import Base


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String(3))

    # Connection with the student. Many to one.
    student: Mapped[list[Student]] = relationship(back_populates="group")
    # Connection with the teacher. Many to many.
    teacher: Mapped[list[Teacher]] = relationship(secondary=teacher_class_association_table, back_populates='group')








