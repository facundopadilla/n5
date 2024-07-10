from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import ORJSONResponse
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import RecordNotFound
from src.database.session import get_session
from src.models.vehicles.model import VehicleModel
from src.models.vehicles.operations import (
    VehicleCreate,
    VehicleFilter,
    VehiclePartialUpdate,
    VehicleRead,
    VehicleUpdate,
)
from src.services.vehicles import VehicleService

router = APIRouter(prefix="/vehicles", tags=["Vehicle"])


@router.get(path="", response_model=VehicleRead, response_class=ORJSONResponse)
async def get_by_id(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Public ID"),
):
    instance: Vehicle = await VehicleService.get_by_id(  # type: ignore
        session=session, id=id,
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=VehicleModel)
    return instance


@router.get(
    path="/filter", response_model=Page[VehicleRead], response_class=ORJSONResponse
)
async def get_paginated(
    session: AsyncSession = Depends(get_session),
    query_params: VehicleFilter = Depends(),
):
    instances = await VehicleService.filter(
        session=session,
        **query_params.model_dump(exclude_none=True)
    )
    return paginate(instances)


@router.post(path="", response_model=VehicleRead, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    session: AsyncSession = Depends(get_session),
    payload: VehicleCreate = Body(..., description="Vehicle model for create"),
):
    instance = await VehicleService.create(session=session, **payload.model_dump())
    return instance


@router.put(path="", response_model=VehicleRead, response_class=ORJSONResponse)
async def update_vehicle(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description=""),
    payload: VehicleUpdate = Body(..., description="Vehicle model for update"),
):
    instance = await VehicleService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=VehicleModel)
    return instance


@router.patch(path="", response_model=VehicleRead, response_class=ORJSONResponse)
async def partial_update_vehicle(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Public ID"),
    payload: VehiclePartialUpdate = Body(
        ..., description="Vehicle model for partial update"
    ),
):
    instance = await VehicleService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=VehicleModel)
    return instance


@router.delete(path="", response_model=VehicleRead, response_class=ORJSONResponse)
async def delete_vehicle(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Vehicle ID"),
):
    instance = await VehicleService.delete_by_id(
        session=session, id=id
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=VehicleModel)

    return instance
