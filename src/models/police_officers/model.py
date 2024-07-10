from src.models.base.fields import BaseSQLModel
from src.models.base.security import PasswordField
from src.models.police_officers.base import PoliceOfficerBase


class PoliceOfficerModel(
    BaseSQLModel,
    PoliceOfficerBase,
    PasswordField,
    table=True
):
    pass
