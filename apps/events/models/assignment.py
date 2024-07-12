from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Column, Integer, Date
from sqlalchemy.sql import func

from datetime import datetime

from apps.group.models.student import Student
from apps.group.models.group import Group

from assigned_tasks import assigned_task_association_table

from db import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    teacher = relationship("User", back_populates="assignments")
    assigned_tasks = relationship("AssignedTask", back_populates="assignment")
