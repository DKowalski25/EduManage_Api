from core import logger
from scripts.db_session import db_session

from apps.users.models import User
from apps.users.storages.user_storage import hash_password, get_random_string

TEACHERS = [
    {"first_name": "Teacher", "last_name": "One", "email": "teacher1@example.com", "phone_number": "9807652123",
     "password": "1234", "role": User.TEACHER},
    {"first_name": "Teacher", "last_name": "Two", "email": "teacher2@example.com", "phone_number": "+79193768291",
     "password": "7896", "role": User.TEACHER},
    {"first_name": "Teacher", "last_name": "Three", "email": "teacher3@example.com", "phone_number": "+79873652123",
     "password": "0000", "role": User.TEACHER},
]


def perform(*args, **kwargs):
    for data in TEACHERS:
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
