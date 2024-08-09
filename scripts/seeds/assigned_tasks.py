from core import logger
from scripts.db_session import db_session

from apps.events.models import AssignedTask, Assignment
from apps.group.models import Group
from apps.users.models import User

ASSIGNED_TASKS = [
    {"assignment_title": "Assignment 1", "group_name": "null", "student_email": "student1@example.com",
     "assigned_at": "2024-01-05"},
    {"assignment_title": "Assignment 2", "group_name": "null", "student_email": "student1@example.com",
     "assigned_at": "2024-01-05"},
    {"assignment_title": "Assignment 3", "group_name": "null", "student_email": "student2@example.com",
     "assigned_at": "2024-01-05"}
]


def perform(*args, **kwargs):
    for data in ASSIGNED_TASKS:
        assignment = db_session.query(Assignment).filter_by(title=data["assignment_title"]).first()
        group = db_session.query(Group).filter_by(group_name=data["group_name"]).first()
        student = db_session.query(User).filter_by(email=data["student_email"]).first()

        if not assignment:
            logger.warning(f"Assignment {data['assignment_title']} not found")
            continue
        if not group:
            logger.warning(f"Group {data['group_name']} not found")
            continue
        if not student:
            logger.warning(f"Student {data['student_email']} not found")
            continue

        assigned_task = AssignedTask(
            assignment_id=assignment.id,
            group_id=group.id,
            student_id=student.id,
            assigned_at=data["assigned_at"]
        )
        db_session.add(assigned_task)
        logger.info(f"AssignedTask for {data['assignment_title']} created")

    db_session.commit()
    db_session.close()
