from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import ORJSONResponse
from fastapi_pagination import Page, paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from src.core.exceptions import RecordNotFound
from src.database.session import get_session
from src.models.police_officers.model import PoliceOfficerModel
from src.models.traffic_violations.model import TrafficViolationModel
from src.models.traffic_violations.operations import (
    TrafficViolationCreate,
    TrafficViolationFilter,
    TrafficViolationPartialUpdate,
    TrafficViolationRead,
    TrafficViolationUpdate,
)
from src.services.traffic_violations import TrafficViolationService
from src.services.people import PeopleService
from src.security.jwt import get_current_user

router = APIRouter(prefix="/traffic_violations", tags=["Traffic violation"])


@router.get(path="", response_model=TrafficViolationRead, response_class=ORJSONResponse)
async def get_by_id(
        session: AsyncSession = Depends(get_session),
        id: int = Query(..., description="Public ID"),
):
    instance: TrafficViolation = await TrafficViolationService.get_by_id(  # type: ignore
        session=session, id=id,
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=TrafficViolationModel)
    return instance


@router.get(
    path="/filter", response_model=Page[TrafficViolationRead], response_class=ORJSONResponse
)
async def get_paginated(
        session: AsyncSession = Depends(get_session),
        query_params: TrafficViolationFilter = Depends(),
):
    instances = await TrafficViolationService.filter(
        session=session,
        **query_params.model_dump(exclude_none=True)
    )
    return paginate(session, instances)


@router.put(path="", response_model=TrafficViolationRead, response_class=ORJSONResponse)
async def update_traffic_violations(
        session: AsyncSession = Depends(get_session),
        id: int = Query(..., description=""),
        payload: TrafficViolationUpdate = Body(..., description="Traffic violation model for update"),
):
    instance = await TrafficViolationService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=TrafficViolationModel)
    return instance


@router.patch(path="", response_model=TrafficViolationRead, response_class=ORJSONResponse)
async def partial_update_traffic_violations(
        session: AsyncSession = Depends(get_session),
        id: int = Query(..., description="Public ID"),
        payload: TrafficViolationPartialUpdate = Body(
            ..., description="Traffic violation model for partial update"
        ),
):
    instance = await TrafficViolationService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=TrafficViolationModel)
    return instance


@router.delete(path="", response_model=TrafficViolationRead, response_class=ORJSONResponse)
async def delete_traffic_violations(
        session: AsyncSession = Depends(get_session),
        id: int = Query(..., description="Traffic violation ID"),
):
    instance = await TrafficViolationService.delete_by_id(
        session=session, id=id
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=TrafficViolationModel)

    return instance


@router.post(path="/cargar_infraccion", response_model=TrafficViolationRead, response_class=ORJSONResponse, status_code=status.HTTP_201_CREATED)
async def create_traffic_violations(
    session: AsyncSession = Depends(get_session),
    police_officer: PoliceOfficerModel = Depends(get_current_user),
    payload: TrafficViolationCreate = Body(..., description="Traffic violation model for create"),
):
    fields = payload.model_dump()
    fields["police_officer_id"] = police_officer.id
    instance = await TrafficViolationService.create(session=session, **fields)
    return instance


@router.get(path="/generar_informe", response_model=Page[TrafficViolationRead], response_class=ORJSONResponse)
async def generar_informe(
        email: EmailStr = Query(...),
        session: AsyncSession = Depends(get_session)
):
    person = await PeopleService.filter(
        session=session,
        first=True,
        email=email
    )
    if not person:
        raise RecordNotFound(
            query_fields={"email": email},
            model=PeopleService.model
        )

    stmt = select(TrafficViolationModel).where(TrafficViolationModel.vehicle_id == person.vehicle.id)
    result = await session.execute(stmt)
    return paginate(result.scalars().all())
