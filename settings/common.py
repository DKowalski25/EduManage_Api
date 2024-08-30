import os
from pathlib import Path

import dotenv

path_to_env = Path(__file__).parents[1].joinpath(".env")

try:
    dotenv.read_dotenv('path_to_env')
except AttributeError:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=path_to_env)

PORT = int(os.environ.get("PORT", 8000))
HOST = os.environ.get("HOST", "0.0.0.0")
ADMIN_PORT = int(os.environ.get("ADMIN_PORT", 5000))
ADMIN_HOST = os.environ.get("ADMIN_HOST", "0.0.0.0")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ENV = os.environ.get("ENV")

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = int(os.environ.get("DB_PORT"))

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")
DB_PORT_TEST = int(os.environ.get("DB_PORT_TEST"))

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')


LOGURU_BACKTRACE = True
LOGURU_DIAGNOSE = True
LOG_LEVEL = "INFO"
LOGURU_FORMAT = (
    "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>]"
    "[<level>{level}</level>] "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n"
)

AUTH_SECRET_KEY = os.environ.get('AUTH_SECRET_KEY')
AUTH_HASHING_ALGORITHM = "HS256"
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('AUTH_ACCESS_TOKEN_EXPIRE_MINUTES'))
AUTH_REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get('AUTH_REFRESH_TOKEN_EXPIRE_MINUTES'))

APP_VERSION = "0.1"
APP_API_NAME = "Edumanage API"
APP_ADMIN_NAME = "Edumanage Admin"
