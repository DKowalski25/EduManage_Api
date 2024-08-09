from core import logger
from scripts.db_session import db_session

from apps.group.models import Group

GROUPS = [
    {"group_name": "Group 1", "description": "This is group 1", "grade": 1},
    {"group_name": "Group 2", "description": "This is group 2", "grade": 2},
]


def perform(*args, **kwargs):
    for data in GROUPS:
        is_group_exists = db_session.query(Group).filter_by(group_name=data["group_name"]).first()
        if not is_group_exists:
            group = Group(
                group_name=data["group_name"],
                description=data["description"],
                grade=data["grade"]
            )
            db_session.add(group)
            logger.info(f"Group {data['group_name']} created")
        else:
            logger.warning(f"Group {data['group_name']} already exists")

    db_session.commit()
    db_session.close()
