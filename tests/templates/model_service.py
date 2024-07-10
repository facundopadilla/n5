from typing import Type
from collections import OrderedDict

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.types.models import Model
from src.services.orm.models import ModelService


def get_random_attr(instance: Model):
    for attr, obj in instance.__dict__.items():
        if (
                attr not in ["id", "_sa_instance_state", "created_at", "updated_at"] and
                isinstance(obj, str)
        ):
            return obj, attr


class ModelServiceTestTemplate:
    model: Model
    service: Type[ModelService]
    fake_dict_fixture: str

    @pytest.fixture
    def fake_dict(self, request) -> dict:
        return request.getfixturevalue(self.fake_dict_fixture)

    async def test_create_successful(self, mock_session: AsyncSession, fake_dict: dict):
        f"""
        This test verifies that the creation of a {str(self.model)} is functioning correctly.
        """
        # region -- Assert __
        instance = await self.service.create(session=mock_session, **fake_dict)
        model_dump = instance.model_dump(mode="json")
        diff = set(fake_dict.keys()).difference(model_dump.keys())
        new_fake_dict = {k: v for k, v in fake_dict.items() if k not in diff}
        new_model_dump = {k: v for k, v in model_dump.items() if k in new_fake_dict.keys()}
        fake_ordered = OrderedDict(sorted(new_fake_dict.items(), key=lambda x: x[0]))
        model_ordered = OrderedDict(sorted(new_model_dump.items(), key=lambda x: x[0]))
        assert model_ordered == fake_ordered
        # endregion
        # region -- Clean up --
        await self.service.delete_by_id(session=mock_session, id=instance.id)
        # endregion

    async def test_delete_by_id_successful(
            self, mock_session: AsyncSession, fake_dict: dict
    ):
        # region -- Assert --
        instance = await self.service.create(session=mock_session, **fake_dict)
        deleted_instance = await self.service.delete_by_id(
            session=mock_session, id=instance.id
        )
        instance_from_db = await self.service.get_by_id(
            session=mock_session, id=instance.id
        )
        assert (deleted_instance == instance) and (instance_from_db is None)
        # endregion

    async def test_update_by_id_successful(
            self,
            mock_session: AsyncSession,
            fake_dict: dict,
    ):
        # region -- Assert --
        instance = await self.service.create(session=mock_session, **fake_dict)
        attr = "name"
        instance_name = getattr(instance, attr, None)
        if not instance_name:
            instance_name, attr = get_random_attr(instance)
        updated_instance = await self.service.update_by_id(  # type: ignore
            session=mock_session, id=instance.id, **{attr: "test"}
        )
        assert getattr(updated_instance, attr) != instance_name  # type: ignore
        # endregion
        # region -- Clean up --
        await self.service.delete_by_id(session=mock_session, id=instance.id)
        # endregion
