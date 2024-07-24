from core import logger
from scripts.db_session import db_session
from apps.users.models import User
from apps.users.storages.user_storage import hash_password, get_random_string

ADMINS = [
    {"username": "admin", "password": "password", "role": "admin", "email": "admin@example.com", "first_name": "Admin",
     "last_name": "User", "phone_number": "1234567890"},
]


def perform(*args, **kwargs):
    for data in ADMINS:
        is_admin_exists = db_session.query(User).filter_by(username=data["username"]).all()
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
            logger.info(f"Admin {data['username']} created")
        else:
            logger.warning(f"Admin {data['username']} already exists")

    db_session.commit()
    db_session.close()
