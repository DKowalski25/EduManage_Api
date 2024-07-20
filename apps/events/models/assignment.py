from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, Column, Integer, Date

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
    teacher = relationship(
        "User",
        back_populates="assignments",
        # lazy="selectin"
    )
    assigned_tasks = relationship(
        "AssignedTask",
        back_populates="assignment",
        # lazy="subquery"
    )
    marks = relationship(
        "Mark",
        back_populates="assignment",
        # lazy="selectin"
    )

    @property
    def awaitable_attrs(self):
        # Возвращаем список атрибутов, которые могут быть получены как awaitable
        return ["teacher", "assigned_tasks", "marks"]
