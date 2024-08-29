import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.internals.orm_internal_service import OrmInternalService
from settings import TEST_DB_URL, TEST_DB_IDEMPOTENT
from settings.development import LOG_ORM
from .containers import db_container


@pytest.fixture(scope='session')
async def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""

    db_url = TEST_DB_URL
    if not db_url:
        raise Exception('Configure db_url via --dburl flag or TEST_DB_URL env')

    engine = create_async_engine(
        db_url,
        echo=LOG_ORM,
        pool_size=100,
        max_overflow=15,
    )

    yield engine
    await engine.dispose()


@pytest.fixture(scope='function')
def db_sessionmaker(db_engine):
    return async_sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope='function')
async def db_session(db_engine, db_sessionmaker):
    """yields a SQLAlchemy connection which is rollbacked after the test"""

    metadata = OrmInternalService.get_models_metadata()
    async with db_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    async with db_sessionmaker() as sess:
        yield sess
        await sess.rollback()


lock = asyncio.Lock()


@pytest.fixture(scope='function')
async def with_db(db_session):
    async with lock:
        with db_container.session.override(db_session):
            yield


@pytest.hookimpl()
def pytest_collection_modifyitems(items):
    if TEST_DB_IDEMPOTENT:
        for item in items:
            if item.get_closest_marker('with_db'):
                item.fixturenames.append('with_db')
