from typing import Any, List, Optional, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DatabaseError
from src.core.logger import logger
from src.core.types.models import Model


class SQLAlchemyService:
    model: Model

    @classmethod
    async def _get_by_field(
        cls,
        session: AsyncSession,
        column: str,
        value: Any
    ) -> Optional[Model]:
        try:
            stmt = select(cls.model).where(column == value)
            result = await session.execute(stmt)
        except Exception as e:
            logger.error(
                f"An error has occurred when trying to get a '{repr(cls.model)}'"
                f" instance with {str(column)}: {value}, error: {e}"
            )
            raise DatabaseError(model=cls.model, exc=e)

        instance = result.scalars().first()
        return instance

    @classmethod
    async def _filter(
        cls, session: AsyncSession, first: bool = False, **fields
    ) -> List[Model] | Model:
        try:
            stmt = select(cls.model)

            for column, value in fields.items():
                column = getattr(cls.model, column)
                stmt = stmt.where(column == value)
            result = await session.execute(stmt)
        except Exception as e:
            logger.error(
                f"An error has occurred when trying to filter in '{repr(cls.model)}' following fields: {fields}"
            )
            raise DatabaseError(model=cls.model, exc=e)
        if first:
            return result.scalars().first()

        return cast(List[Model], result.scalars().all())

    @classmethod
    async def _create(cls, session: AsyncSession, **fields) -> Model:
        try:
            instance = cls.model(**fields)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
        except Exception as e:
            logger.error(
                f"An error as occurred when try to create a '{repr(cls.model)}'"
                f" instance, error: {e}"
            )
            await session.rollback()
            raise DatabaseError(model=cls.model, exc=e)

        return cast(Model, instance)

    @classmethod
    async def _update(
        cls, session: AsyncSession, instance: Model, **fields_to_update
    ) -> Model:
        for field, new_value in fields_to_update.items():
            setattr(instance, field, new_value)

        try:
            await session.commit()
            await session.refresh(instance)
        except Exception as e:
            logger.error(
                f"An error as occurred when try to update a '{repr(cls.model)}'"
                f" instance, error: {e}"
            )
            await session.rollback()
            raise DatabaseError(model=cls.model, exc=e)
        return instance

    @classmethod
    async def _delete(cls, session: AsyncSession, instance: Model) -> Model:
        try:
            await session.delete(instance)
            await session.commit()
        except Exception as e:
            logger.error(
                f"An error as occurred when try to delete a '{repr(cls.model)}'"
                f" instance, error: {e}"
            )
            await session.rollback()
            raise DatabaseError(model=cls.model, exc=e)

        return instance
