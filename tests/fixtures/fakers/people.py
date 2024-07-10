from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.people.model import PeopleModel
from src.services.people import PeopleService

from .decorators import inject_params
from .utils import create_dict_from_model


@pytest.fixture
@inject_params
def fake_people_dict(request) -> dict:
    return create_dict_from_model(PeopleModel, **request.param)


@pytest.fixture
async def fake_people(
    mock_session: AsyncSession, fake_people_dict: dict
) -> AsyncGenerator[PeopleModel, None]:
    instance = await PeopleService.create(session=mock_session, **fake_people_dict)
    yield instance  # type: ignore
    await PeopleService.delete_by_id(session=mock_session, id=instance.id)
