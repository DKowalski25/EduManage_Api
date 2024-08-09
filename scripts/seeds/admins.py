from core import logger
from scripts.db_session import db_session

from apps.users.models import User
from apps.users.storages.user_storage import hash_password, get_random_string

ADMINS = [
    {"first_name": "Admin", "last_name": "Admin", "email": "admin@example.com", "phone_number": "1234567890",
     "password": "password", "role": "admin"},
]


def perform(*args, **kwargs):
    for data in ADMINS:
        is_admin_exists = db_session.query(User).filter_by(
            first_name=data['first_name'],
            last_name=data['last_name'],
        ).all()

        salt = get_random_string()

        if not is_admin_exists:
            admin = {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "email": data["email"],
                "phone_number": data["phone_number"],
                "role": data["role"],
                "hashed_password": f"{salt}${hash_password(data['password'], salt)}",
            }
            db_session.add(User(**admin))
            logger.info(f"Admin {data['first_name']} {data['last_name']} created")
        else:
            logger.warning(f"Admin {data['first_name']} {data['last_name']} already exists")

    db_session.commit()
    db_session.close()
