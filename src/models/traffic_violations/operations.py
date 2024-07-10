from pydantic_partial import create_partial_model

from src.models.traffic_violations.base import TrafficViolationBase
from src.models.base.fields import CreatedAndUpdatedField, IdField


class TrafficViolationCreate(TrafficViolationBase):
    pass


class TrafficViolationUpdate(TrafficViolationBase):
    pass


class TrafficViolationRead(TrafficViolationBase, IdField, CreatedAndUpdatedField):
    vehicle_id: int


class _TrafficViolationFilter(TrafficViolationBase, IdField, CreatedAndUpdatedField):
    pass


TrafficViolationPartialUpdate = create_partial_model(TrafficViolationUpdate)
TrafficViolationFilter = create_partial_model(_TrafficViolationFilter)
