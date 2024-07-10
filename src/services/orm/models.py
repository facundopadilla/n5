from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.types.models import Model
from src.services.orm.sqlalchemy import SQLAlchemyService


class ModelService(SQLAlchemyService):
    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> Model | None:
        return await cls._get_by_field(
            session=session,
            column=cls.model.id,
            value=id,
        )

    @classmethod
    async def filter(
            cls, session: AsyncSession, first: bool = False, **fields
    ) -> Model | List[Model]:
        return await cls._filter(
            session=session, first=first, **fields
        )

    @classmethod
    async def create(cls, session: AsyncSession, **fields: Model) -> Model:
        return await cls._create(session=session, **fields)

    @classmethod
    async def update_by_id(
            cls, session: AsyncSession, id: int, **fields_to_update
    ) -> Model | None:
        instance = await cls.get_by_id(session=session, id=id)
        if instance is None:
            return None

        return await cls._update(session=session, instance=instance, **fields_to_update)

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id: int) -> Model | None:
        instance = await cls.get_by_id(session=session, id=id)
        if instance is None:
            return None

        return await cls._delete(session=session, instance=instance)
