from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer, Date


from apps.events.models.teacher_class import teacher_class_association_table


from db import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    group_name = Column(String, nullable=False)
    description = Column(String)
    grade = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)

    # Relationships
    teachers = relationship(
        "User",
        secondary=teacher_class_association_table,
        back_populates="classes"
    )
    students = relationship("User", back_populates="group", foreign_keys="[User.group_id]")
    assigned_tasks = relationship("AssignedTask", back_populates="group")
