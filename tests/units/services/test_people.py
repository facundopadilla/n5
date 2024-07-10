import pytest

from src.services.people import PeopleService
from tests.templates.model_service import ModelServiceTestTemplate


@pytest.mark.unit
@pytest.mark.service
@pytest.mark.people
class TestPeopleService(ModelServiceTestTemplate):
    model = PeopleService.model
    service = PeopleService
    fake_dict_fixture = "fake_people_dict"
