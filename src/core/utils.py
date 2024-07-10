from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.types.models import Model
from src.core.exceptions import RecordNotFound
from src.services.orm.models import ModelService


async def get_or_404(
    session: AsyncSession,
    model_service: Type[ModelService],
    id: int
) -> Model:
    instance = await model_service.get_by_id(session=session, id=id)
    if instance is None:
        raise RecordNotFound(
            query_fields={"id": id},
            model=model_service.model
        )
    return instance
