import asyncio

import httpx
import pytest

from .internals import get_application


@pytest.fixture(scope='session')
async def client():
    async with httpx.AsyncClient(app=get_application(), base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
