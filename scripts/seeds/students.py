from core import logger
from scripts.db_session import db_session

from apps.users.models import User
from apps.users.storages.user_storage import hash_password, get_random_string


STUDENTS = [
    {"first_name": "Student", "last_name": "One", "email": "student1@example.com", "phone_number": "+79837652123",
     "password": "9801", "role": User.STUDENT},
    {"first_name": "Student", "last_name": "Two", "email": "student2@example.com", "phone_number": "+79193768291",
     "password": "7896", "role": User.STUDENT},
]


def perform(*args, **kwargs):
    for data in STUDENTS:
        is_teacher_exists = db_session.query(User).filter_by(email=data["email"]).all()
        salt = get_random_string()

        if not is_teacher_exists:
            teacher = {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "email": data["email"],
                "phone_number": data["phone_number"],
                "role": data["role"],
                "hashed_password": f"{salt}${hash_password(data['password'], salt)}",
            }
            db_session.add(User(**teacher))
            logger.info(f"Teacher {data['email']} created")
        else:
            logger.warning(f"Teacher {data['email']} already exists")

    db_session.commit()
    db_session.close()
