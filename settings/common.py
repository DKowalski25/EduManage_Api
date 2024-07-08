import os
from typing import Final

from dotenv import load_dotenv

from core import EnvDependNotFound

load_dotenv()


def get_env_var(var_name: str) -> str:
    """
    :raise EnvDependNotFound if value in None
    :param var_name: Env var name
    :return: Var value by name
    """
    value: str | None = os.getenv(var_name)
    if value is None:
        raise EnvDependNotFound(var_name)
    else:
        return value


HOST: Final[str] = get_env_var("HOST")
PORT: Final[int] = int(get_env_var("PORT"))

DB_USER: Final[str] = get_env_var("DB_USER")
DB_HOST: Final[str] = get_env_var("DB_HOST")
DB_PASS: Final[str] = get_env_var("DB_PASS")
DB_NAME: Final[str] = get_env_var("DB_NAME")
DB_PORT: Final[str] = get_env_var("DB_PORT")

# For tests
# USERNAME_TEST_DB: Final[str] = get_env_var("USERNAME_TEST_DB")
# HOST_TEST_DB: Final[str] = get_env_var("HOST_TEST_DB")
# PASSWORD_TEST_DB: Final[str] = get_env_var("PASSWORD_TEST_DB")
# DATABASE_TEST_NAME: Final[str] = get_env_var("DATABASE_TEST_NAME")
# PORT_TEST_DB: Final[str] = get_env_var("PORT_TEST_DB")
