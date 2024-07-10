from typing import Optional

from sqlmodel import Field

from pydantic_partial import create_partial_model

from src.models.vehicles.base import VehicleBase
from src.models.base.fields import CreatedAndUpdatedField, IdField

from src.models.people.operations import PeopleRead


class VehicleCreate(VehicleBase):
    owner_id: Optional[int] = Field(
        default=None,
        description="Person ID",
        gt=0
    )


class VehicleUpdate(VehicleBase):
    pass


class VehicleRead(VehicleBase, IdField, CreatedAndUpdatedField):
    owner: Optional[PeopleRead]


class _VehicleFilter(VehicleBase, IdField, CreatedAndUpdatedField):
    pass


VehiclePartialUpdate = create_partial_model(VehicleUpdate, recursive=True)
VehicleFilter = create_partial_model(_VehicleFilter, recursive=True)
