import datetime

import pytest
import httpx
from passlib.hash import pbkdf2_sha256 as sha256

from src.services.police_officers import PoliceOfficerService
from src.services.vehicles import VehicleService


class BearerAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = "Bearer " + self.token
        yield request


class TestTrafficViolationIntegration:
    URL = "/api/v1/traffic_violations"

    @pytest.fixture
    async def mock_jwt(self, async_client: httpx.AsyncClient, mock_session, fake_police_officer):
        password = "test"
        await PoliceOfficerService.update_by_id(
            session=mock_session,
            id=fake_police_officer.id,
            password=sha256.hash(password)
        )
        rsps = await async_client.post(
            url="/api/v1/token",
            data={
                "username": fake_police_officer.badge,
                "password": password
            }
        )
        access_token = rsps.json()["access_token"]

        yield BearerAuth(access_token)

    async def test_cargar_infraccion(
            self,
            async_client: httpx.AsyncClient,
            fake_police_officer,
            fake_vehicle,
            fake_people,
            mock_jwt
    ):
        # region -- Setup --
        payload = {
            "license_plate": fake_vehicle.license_plate,
            "timestamp": str(datetime.datetime.now().date()),
            "comment": "test"
        }
        # endregion
        # region -- Assert --
        rsps = await async_client.post(
            url=self.URL + "/cargar_infraccion",
            json=payload,
            auth=mock_jwt
        )
        assert rsps.status_code == 201
        # endregion
        # region -- Clean up --
        rsps = await async_client.delete(
            url=self.URL,
            params={
                "id": 1
            }
        )
        assert rsps.status_code == 200
        # endregion

    async def test_obtener_informe(
        self,
        async_client: httpx.AsyncClient,
        fake_vehicle_dict,
        fake_people_dict,
        mock_jwt
    ):
        # region -- Setup --
        API_PEOPLE = "/api/v1/people"
        API_VEHICLES = "/api/v1/vehicles"
        # First step, create a person

        first_rsps = await async_client.post(
            url="/api/v1/people",
            json=fake_people_dict
        )
        # Second step, create a vehicle and link with the person
        owner_id = first_rsps.json()["id"]
        fake_vehicle_dict["owner_id"] = owner_id
        second_rsps = await async_client.post(
            url="/api/v1/vehicles",
            json=fake_vehicle_dict
        )
        vehicle_id = second_rsps.json()["id"]
        license_plate = second_rsps.json()["license_plate"]
        payload = {
            "license_plate": license_plate,
            "timestamp": str(datetime.datetime.now().date()),
            "comment": "test"
        }
        # endregion
        # region -- Assert --
        for i in range(3):
            payload["comment"] += str(i)
            rsps = await async_client.post(
                url=self.URL + "/cargar_infraccion",
                json=payload,
                auth=mock_jwt
            )
            assert rsps.status_code == 201

        rsps = await async_client.get(
            url=self.URL + "/generar_informe",
            params={
                "email": fake_people_dict["email"]
            },
        )
        data = rsps.json()
        assert rsps.status_code == 200 and data["total"] == 3
        # endregion
        # region -- Clean up --
        del_vehicle = await async_client.delete(
            url=API_VEHICLES,
            params={"id": vehicle_id}
        )
        del_person = await async_client.delete(
            url=API_PEOPLE,
            params={"id": owner_id}
        )
        assert 200 in [del_person.status_code, del_vehicle.status_code]
        # endregion