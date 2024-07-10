from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.types.models import Model
from src.core.utils import get_or_404

from src.models.vehicles.model import VehicleModel
from src.services.orm.models import ModelService
from src.services.people import PeopleService


class VehicleService(ModelService):
    model = VehicleModel

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        owner_id: Optional[int] = None,
        **vehicle_fields
    ):
        if owner_id:
            owner = await get_or_404(
                session=session,
                model_service=PeopleService,
                id=owner_id
            )
            vehicle_fields["owner_id"] = owner.id

        return await super().create(session=session, **vehicle_fields)

    @classmethod
    async def update_by_id(
        cls,
        session: AsyncSession,
        id: int,
        owner_id: Optional[int],
        **fields_to_update
    ):
        if owner_id:
            owner = await get_or_404(
                session=session,
                model_service=PeopleService,
                id=owner_id
            )
            fields_to_update["owner_id"] = owner.id
        return await super().update_by_id(session=session, id=id, **fields_to_update)
