from core import logger
from scripts.db_session import db_session

from apps.events.models import Assignment
from apps.users.models import User

ASSIGNMENTS = [
    {"title": "Assignment 1", "description": "Description 1", "created_at": "2024-01-01", "due_date": "2024-01-10",
     "teacher_email": "teacher1@example.com", "type": "homework"},
    {"title": "Assignment 2", "description": "Description 2", "created_at": "2024-01-01", "due_date": "2024-01-10",
     "teacher_email": "teacher2@example.com", "type": "exam"},
    {"title": "Assignment 3", "description": "Description 3", "created_at": "2024-01-01", "due_date": "2024-01-10",
     "teacher_email": "teacher2@example.com", "type": "credit"}
]


def perform(*args, **kwargs):
    for data in ASSIGNMENTS:
        teacher = db_session.query(User).filter_by(email=data["teacher_email"]).first()
        if not teacher:
            logger.warning(f"Teacher {data['teacher_email']} not found")
            continue

        assignment = Assignment(
            title=data["title"],
            description=data["description"],
            created_at=data["created_at"],
            due_date=data["due_date"],
            teacher_id=teacher.id,
            type=data["type"]
        )
        db_session.add(assignment)
        logger.info(f"Assignment {data['title']} created")

    db_session.commit()
    db_session.close()
