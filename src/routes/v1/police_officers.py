from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import ORJSONResponse
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import RecordNotFound
from src.database.session import get_session
from src.models.police_officers.model import PoliceOfficerModel
from src.models.police_officers.operations import (
    PoliceOfficerCreate,
    PoliceOfficerFilter,
    PoliceOfficerPartialUpdate,
    PoliceOfficerRead,
    PoliceOfficerUpdate,
)
from src.services.police_officers import PoliceOfficerService

router = APIRouter(prefix="/police_officers", tags=["Police officer"])


@router.get(path="", response_model=PoliceOfficerRead, response_class=ORJSONResponse)
async def get_by_id(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Public ID"),
):
    instance: PoliceOfficer = await PoliceOfficerService.get_by_id(  # type: ignore
        session=session, id=id,
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PoliceOfficerModel)
    return instance


@router.get(
    path="/filter", response_model=Page[PoliceOfficerRead], response_class=ORJSONResponse
)
async def get_paginated(
    session: AsyncSession = Depends(get_session),
    query_params: PoliceOfficerFilter = Depends(),
):
    instances = await PoliceOfficerService.filter(
        session=session,
        **query_params.model_dump(exclude_none=True)
    )
    return paginate(instances)


@router.post(path="", response_model=PoliceOfficerRead, status_code=status.HTTP_201_CREATED)
async def create_police_officer(
    session: AsyncSession = Depends(get_session),
    payload: PoliceOfficerCreate = Body(..., description="Police officer model for create"),
):
    instance = await PoliceOfficerService.create(session=session, **payload.model_dump())
    return instance


@router.put(path="", response_model=PoliceOfficerRead, response_class=ORJSONResponse)
async def update_police_officer(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description=""),
    payload: PoliceOfficerUpdate = Body(..., description="Police officer model for update"),
):
    instance = await PoliceOfficerService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PoliceOfficerModel)
    return instance


@router.patch(path="", response_model=PoliceOfficerRead, response_class=ORJSONResponse)
async def partial_update_police_officer(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Public ID"),
    payload: PoliceOfficerPartialUpdate = Body(
        ..., description="Police officer model for partial update"
    ),
):
    instance = await PoliceOfficerService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PoliceOfficerModel)
    return instance


@router.delete(path="", response_model=PoliceOfficerRead, response_class=ORJSONResponse)
async def delete_police_officer(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Police officer ID"),
):
    instance = await PoliceOfficerService.delete_by_id(
        session=session, id=id
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PoliceOfficerModel)

    return instance
