import httpx
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import powerset_dict


@pytest.mark.integration
@pytest.mark.vehicle
class TestVehicleIntegration:
    URL = "/api/v1/vehicles"

    async def test_create_successful(
        self,
        async_client: httpx.AsyncClient,
        mock_session: AsyncSession,
        fake_vehicle_dict: dict
    ):
        # region -- Setup --
        # endregion
        # region -- Assert --
        rsps = await async_client.post(url=self.URL, json=fake_vehicle_dict)
        assert rsps.status_code == 201
        # endregion
        # region -- Clean up --
        id = rsps.json()["id"]
        rsps = await async_client.delete(url=self.URL + f"?id={id}")
        assert rsps.status_code == 200
        # endregion

    async def test_vehicle_filter(
            self,
            async_client: httpx.AsyncClient,
            mock_session: AsyncSession,
            fake_vehicle
    ):
        # region -- Setup --
        exclude = ["created_at", "updated_at"]
        powerset = powerset_dict(fake_vehicle.model_dump(exclude=exclude, exclude_none=True))
        # region -- Assert --
        for query_params in powerset:
            rsps = await async_client.get(
                url=self.URL + "/filter", params=query_params
            )
            expected_response = fake_vehicle.model_dump(exclude=exclude, exclude_none=True)
            data = rsps.json()
            items = {
                k: v
                for k, v in data["items"][0].items()
                if k not in exclude
            }
            del items["owner"]
            assert rsps.status_code == 200 and items == expected_response
        # region -- Clean up --
        # Deleted by fixture
        # endregion

    async def test_vehicle_not_exists(
            self, async_client: httpx.AsyncClient, mock_session: AsyncSession
    ):
        id = 1
        expected_rsps = {
            "detail": "Vehicle not found",
            "query_fields": {"id": id},
        }
        rsps = await async_client.get(url=self.URL, params={"id": id})
        assert rsps.status_code == 404 and (rsps.json() == expected_rsps)

    async def test_delete_vehicle_not_exists(
            self, async_client: httpx.AsyncClient, mock_session: AsyncSession
    ):
        id = 1
        expected_rsps = {
            "detail": "Vehicle not found",
            "query_fields": {"id": id},
        }
        rsps = await async_client.delete(url=self.URL, params={"id": id})
        assert rsps.status_code == 404 and (rsps.json() == expected_rsps)