from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import RecordNotFound
from src.core.types.models import Model
from src.models.traffic_violations.model import TrafficViolationModel

from src.services.vehicles import VehicleService
from src.services.orm.models import ModelService


class TrafficViolationService(ModelService):
    model = TrafficViolationModel

    @classmethod
    async def create(  # noqa
        cls,
        session: AsyncSession,
        license_plate: str,
        **traffic_violation_fields
    ) -> Model:
        vehicle = await VehicleService.filter(
            session=session,
            license_plate=license_plate,
            first=True
        )
        if not vehicle:
            raise RecordNotFound(
                query_fields={"license_plate": license_plate},
                model=VehicleService.model
            )
        traffic_violation_fields["license_plate"] = license_plate
        traffic_violation_fields["vehicle_id"] = vehicle.id
        return await super().create(session=session, **traffic_violation_fields)
