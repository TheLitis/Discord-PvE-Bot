import asyncio
import pytest
from utils.db import async_session_maker, Base, engine
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture(scope="module")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_db_connection(setup_db):
    async with async_session_maker() as session:
        assert isinstance(session, AsyncSession)