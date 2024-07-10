from pydantic_partial import create_partial_model

from src.models.base.security import PasswordField
from src.models.police_officers.base import PoliceOfficerBase
from src.models.base.fields import CreatedAndUpdatedField, IdField


class PoliceOfficerCreate(PoliceOfficerBase, PasswordField):
    pass


class PoliceOfficerUpdate(PoliceOfficerBase):
    pass


class PoliceOfficerRead(PoliceOfficerBase, IdField, CreatedAndUpdatedField):
    pass


class _PoliceOfficerFilter(PoliceOfficerBase, IdField, CreatedAndUpdatedField):
    pass


PoliceOfficerPartialUpdate = create_partial_model(PoliceOfficerUpdate)
PoliceOfficerFilter = create_partial_model(_PoliceOfficerFilter)
