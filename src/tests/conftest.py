import asyncio
import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base, engine, async_session
from main import app
from models import Balance, Reserved


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        yield client


@pytest_asyncio.fixture(scope='function')
async def session() -> AsyncSession:
    async with async_session() as s:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope='function')
async def balance():
    async with async_session() as s:
        async with s.begin():
            stmt = insert(Balance).values({'user_id': uuid.uuid4(), 'money': 5}).returning(*Balance.returning())
            res = await s.execute(stmt)
            b = res.fetchone()

    yield b


@pytest_asyncio.fixture(scope='function')
async def reserved():
    async with async_session() as s:
        async with s.begin():
            user_id = uuid.uuid4()
            stmt = insert(Balance).values({'user_id': user_id, 'money': 4})

            await s.execute(stmt)

            stmt = (
                insert(Reserved)
                .values(balance_id=user_id, order_id=uuid.uuid4(), service_id=uuid.uuid4(), money=1)
                .returning(*Reserved.returning())
            )
            res = await s.execute(stmt)
            r = res.fetchone()

    yield r
