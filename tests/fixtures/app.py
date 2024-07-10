from typing import AsyncGenerator

import httpx
import pytest

from src.main import app


@pytest.fixture
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(
        app=app, base_url="http://test", follow_redirects=True
    ) as client:
        yield client
