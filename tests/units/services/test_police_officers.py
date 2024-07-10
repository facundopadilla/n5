import pytest

from src.models.police_officers.model import PoliceOfficerModel
from src.services.police_officers import PoliceOfficerService
from tests.templates.model_service import ModelServiceTestTemplate


@pytest.mark.unit
@pytest.mark.service
@pytest.mark.police_officers
class TestPoliceOfficerService(ModelServiceTestTemplate):
    model = PoliceOfficerModel
    service = PoliceOfficerService
    fake_dict_fixture = "fake_police_officer_dict"
