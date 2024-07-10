import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.session import get_session
from src.main import app


@pytest.fixture(scope="function", autouse=True)
async def mock_session(mock_engine_async: AsyncEngine):
    session_factory = sessionmaker(  # noqa
        bind=mock_engine_async,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async_session = session_factory()

    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_session] = override_get_session  # noqa

    yield async_session
