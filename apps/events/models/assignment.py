import enum

from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, Column, Integer, Date, Enum as SQLAlchemyEnum

from db import Base


class AssignmentType(enum.Enum):
    exam = 'exam'
    credit = 'credit'
    homework = 'homework'


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(SQLAlchemyEnum(AssignmentType, name="assignmenttype"), nullable=False)

    # Relationships
    teacher = relationship(
        "User",
        back_populates="assignments",
    )
    assigned_tasks = relationship(
        "AssignedTask",
        back_populates="assignment",
    )
    marks = relationship(
        "Mark",
        back_populates="assignment",
    )
