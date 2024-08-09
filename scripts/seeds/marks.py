from core import logger
from scripts.db_session import db_session

from apps.events.models import Mark, Assignment
from apps.users.models import User

MARKS = [
    {"value": 5, "student_email": "student1@example.com", "assignment_title": "Assignment 1", "date": "2024-01-15"},
    {"value": 4, "student_email": "student1@example.com", "assignment_title": "Assignment 2", "date": "2024-01-15"},
    {"value": 3, "student_email": "student2@example.com", "assignment_title": "Assignment 3", "date": "2024-01-15"},
]


def perform(*args, **kwargs):
    for data in MARKS:
        student = db_session.query(User).filter_by(email=data["student_email"]).first()
        assignment = db_session.query(Assignment).filter_by(title=data["assignment_title"]).first()

        if not student:
            logger.warning(f"Student {data['student_email']} not found")
            continue
        if not assignment:
            logger.warning(f"Assignment {data['assignment_title']} not found")
            continue

        mark = Mark(
            value=data["value"],
            student_id=student.id,
            assignment_id=assignment.id,
            date=data["date"]
        )
        db_session.add(mark)
        logger.info(f"Mark for {data['student_email']} created")

    db_session.commit()
    db_session.close()
