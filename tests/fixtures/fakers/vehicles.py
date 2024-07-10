from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.vehicles.model import VehicleModel
from src.services.vehicles import VehicleService

from .decorators import inject_params
from .utils import create_dict_from_model


@pytest.fixture
@inject_params
def fake_vehicle_dict(request) -> dict:
    return create_dict_from_model(VehicleModel, **request.param)


@pytest.fixture
async def fake_vehicle(
    mock_session: AsyncSession, fake_vehicle_dict: dict
) -> AsyncGenerator[VehicleModel, None]:
    instance = await VehicleService.create(session=mock_session, **fake_vehicle_dict)
    yield instance  # type: ignore
    await VehicleService.delete_by_id(session=mock_session, id=instance.id)
