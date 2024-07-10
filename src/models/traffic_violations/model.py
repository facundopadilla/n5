from sqlmodel import Field

from src.models.base.fields import BaseSQLModel
from src.models.traffic_violations.base import TrafficViolationBase


class TrafficViolationModel(BaseSQLModel, TrafficViolationBase, table=True):
    vehicle_id: int = Field(
        default=...,
        foreign_key="vehicles.id",
        description="Vehicle ID"
    )
    police_officer_id: int = Field(
        default=...,
        foreign_key="police_officers.id",
        description="Police officer ID"
    )
