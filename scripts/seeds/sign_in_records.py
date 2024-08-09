from core import logger
from scripts.db_session import db_session
from datetime import datetime

from apps.users.models import User
from apps.users.features.auth.models import SignInRecord


def perform(*args, **kwargs):
    # Получаем всех пользователей из базы данных
    users = db_session.query(User).all()

    if not users:
        logger.warning("No users found to create sign-in records.")
        return

    for user in users:
        # Создаем запись для каждого пользователя
        sign_in_record = SignInRecord(
            user_id=user.id,
            signed_in_at=datetime.now()
        )
        db_session.add(sign_in_record)
        logger.info(f"Sign-in record created for user {user.email}")

    db_session.commit()
    db_session.close()
