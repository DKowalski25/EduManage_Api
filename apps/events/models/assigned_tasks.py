from sqlalchemy import Column, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship

from db import Base


class AssignedTask(Base):
    __tablename__ = "assigned_tasks"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    assigned_at = Column(Date, nullable=False)

    # Relationships
    assignment = relationship("Assignment", back_populates="assigned_tasks")
    group = relationship("Group", back_populates="assigned_tasks")
    student = relationship("User", back_populates="assigned_tasks")
