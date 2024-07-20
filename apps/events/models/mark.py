from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db import Base


class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship(
        "User",
        back_populates="marks",
        # lazy="subquery"
    )
    assignment = relationship(
        "Assignment",
        back_populates="marks",
        # lazy="subquery"
    )

    @property
    def awaitable_attrs(self):
        # Возвращаем список атрибутов, которые могут быть получены как awaitable
        return ["student", "assignment"]
