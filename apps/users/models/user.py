from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer, DateTime, Table, ForeignKey
from sqlalchemy.sql import func

from db import Base

teacher_class_association_table = Table(
    "teacher_class_association_table",
    Base.metadata,
    Column('teacher_id', ForeignKey("users.id"), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    TEACHER = "teacher"
    STUDENT = "student"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(Integer, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    classes = relationship(
        "Group",
        secondary=teacher_class_association_table,
        back_populates="teachers"
    )
    assignments = relationship("Assignment", back_populates="teacher")
    assigned_tasks = relationship("AssignedTask", back_populates="student")
    marks = relationship("Mark", back_populates="student")
