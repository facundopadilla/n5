from typing import Optional

from sqlmodel import Relationship

from src.models.people.base import PeopleBase
from src.models.base.fields import BaseSQLModel


class PeopleModel(PeopleBase, BaseSQLModel, table=True):
    vehicle: "VehicleModel" = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={
            "uselist": False,
            "lazy": "joined"
        }
    )
