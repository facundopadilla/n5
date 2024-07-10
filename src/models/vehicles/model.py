from typing import Optional

from sqlmodel import Relationship, Field

from src.models.base.fields import BaseSQLModel
from src.models.vehicles.base import VehicleBase


class VehicleModel(VehicleBase, BaseSQLModel, table=True):
    owner_id: Optional[int] = Field(
        default=None,
        foreign_key="people.id",
        unique=True
    )
    owner: Optional["PeopleModel"] = Relationship(
        back_populates="vehicle",
        sa_relationship_kwargs={
            "uselist": False,
            "lazy": "selectin"
        }
    )
