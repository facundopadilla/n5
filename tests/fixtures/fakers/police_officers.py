from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.police_officers.model import PoliceOfficerModel
from src.services.police_officers import PoliceOfficerService

from .decorators import inject_params
from .utils import create_dict_from_model


@pytest.fixture
@inject_params
def fake_police_officer_dict(request) -> dict:
    return create_dict_from_model(PoliceOfficerModel, **request.param)


@pytest.fixture
async def fake_police_officer(
    mock_session: AsyncSession, fake_police_officer_dict: dict
) -> AsyncGenerator[PoliceOfficerModel, None]:
    instance = await PoliceOfficerService.create(session=mock_session, **fake_police_officer_dict)
    yield instance  # type: ignore
    await PoliceOfficerService.delete_by_id(session=mock_session, id=instance.id)
