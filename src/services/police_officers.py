from src.models.police_officers.model import PoliceOfficerModel
from src.services.orm.models import ModelService


class PoliceOfficerService(ModelService):
    model = PoliceOfficerModel

