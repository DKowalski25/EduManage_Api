from sqlalchemy import Table, Column, ForeignKey

from db import Base

assigned_task_association_table = Table(
    'assigned_task_association_table',
    Base.metadata,
    Column('task_id', ForeignKey('tasks.id'), primary_key=True),
    Column('student_id', ForeignKey('students.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True)
)
