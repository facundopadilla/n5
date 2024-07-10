import pytest

from src.models.vehicles.model import VehicleModel
from src.services.vehicles import VehicleService
from tests.templates.model_service import ModelServiceTestTemplate


@pytest.mark.unit
@pytest.mark.service
@pytest.mark.vehicles
class TestVehicleService(ModelServiceTestTemplate):
    model = VehicleModel
    service = VehicleService
    fake_dict_fixture = "fake_vehicle_dict"
