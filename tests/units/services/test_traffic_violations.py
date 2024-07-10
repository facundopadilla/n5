from datetime import datetime, date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.traffic_violations import TrafficViolationService


@pytest.mark.unit
@pytest.mark.service
@pytest.mark.traffic_violations
class TestTrafficViolationService():
    model = TrafficViolationService.model
    service = TrafficViolationService
    fake_dict_fixture = "fake_traffic_violations_dict"

    async def test_create_successful(  # noqa
        self,
        mock_session: AsyncSession,
        fake_vehicle,
        fake_police_officer,
        fake_traffic_violations_dict,
    ):
        # region -- Setup --
        if isinstance(fake_traffic_violations_dict.get("timestamp"), str):
            fake_traffic_violations_dict["timestamp"] = datetime.strptime(fake_traffic_violations_dict["timestamp"], "%Y-%m-%d").date()
        fake_traffic_violations_dict["police_officer_id"] = fake_police_officer.id
        # endregion
        # region -- Assert --
        instance = await TrafficViolationService.create(
            session=mock_session,
            **fake_traffic_violations_dict
        )
        assert instance
        # endregion
        # region -- Clean up --
        await TrafficViolationService.delete_by_id(session=mock_session, id=instance.id)
        # endregion
