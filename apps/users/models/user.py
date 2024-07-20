from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from apps.events.models.teacher_class import teacher_class_association_table

from db import Base


class User(Base):
    __tablename__ = "users"

    TEACHER = "teacher"
    STUDENT = "student"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    group_id = Column(Integer, ForeignKey("groups.id"))

    # Relationships
    classes = relationship(
        "Group",
        secondary=teacher_class_association_table,
        back_populates="teachers",
    )
    assignments = relationship(
        "Assignment",
        back_populates="teacher",
    )
    assigned_tasks = relationship(
        "AssignedTask",
        back_populates="student",
    )
    marks = relationship(
        "Mark",
        back_populates="student",
    )
    group = relationship(
        "Group",
        back_populates="students",
        foreign_keys=[group_id],
    )
