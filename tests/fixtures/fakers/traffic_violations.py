from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.traffic_violations.model import TrafficViolationModel
from src.services.traffic_violations import TrafficViolationService

from .decorators import inject_params
from .utils import create_dict_from_model


@pytest.fixture
@inject_params
def fake_traffic_violations_dict(request) -> dict:
    return create_dict_from_model(TrafficViolationModel, **request.param)


@pytest.fixture
async def fake_traffic_violations(
    mock_session: AsyncSession, fake_traffic_violations_dict: dict, fake_vehicle
) -> AsyncGenerator[TrafficViolationModel, None]:
    fake_traffic_violations_dict["vehicle_id"] = fake_vehicle.id
    fake_traffic_violations_dict["license_plate"] = fake_vehicle.license_plate
    instance = await TrafficViolationService.create(session=mock_session, **fake_traffic_violations_dict)
    yield instance  # type: ignore
    await TrafficViolationService.delete_by_id(session=mock_session, id=instance.id)
