import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from core import OrmInternalService, get_application
from db import async_session, Base
from settings import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
                      DB_USER_TEST)
# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker_test = async_sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

OrmInternalService.get_models_metadata()
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session


# @pytest.fixture(scope="session")
# def override_async_session():
#     """Переопределяет стандартный async_session для использования тестовой базы данных."""
#     return async_session_maker_test


@pytest.fixture(scope="session")
def app():
    """Creates a FastAPI application with an overridden database session for tests."""
    _app = get_application()
    _app.dependency_overrides[async_session] = override_get_async_session
    return _app


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client(app) -> TestClient:
    """Возвращает синхронного клиента для тестирования."""
    return TestClient(app)


@pytest.fixture(scope="session")
async def ac(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


