from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import ORJSONResponse
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import RecordNotFound
from src.database.session import get_session
from src.models.people.model import PeopleModel
from src.models.people.operations import (
    PeopleCreate,
    PeopleFilter,
    PeoplePartialUpdate,
    PeopleRead,
    PeopleUpdate,
)
from src.services.people import PeopleService

router = APIRouter(prefix="/people", tags=["People"])


@router.get(path="", response_model=PeopleRead, response_class=ORJSONResponse)
async def get_by_id(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Public ID"),
):
    instance: People = await PeopleService.get_by_id(  # type: ignore
        session=session, id=id,
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PeopleModel)
    print(instance.vehicle)
    return instance


@router.get(
    path="/filter", response_model=Page[PeopleRead], response_class=ORJSONResponse
)
async def get_paginated(
    session: AsyncSession = Depends(get_session),
    query_params: PeopleFilter = Depends(),
):
    instances = await PeopleService.filter(
        session=session,
        **query_params.model_dump(exclude_none=True)
    )
    return paginate(instances)


@router.post(path="", response_model=PeopleRead, status_code=status.HTTP_201_CREATED)
async def create_person(
    session: AsyncSession = Depends(get_session),
    payload: PeopleCreate = Body(..., description="People model for create"),
):
    instance = await PeopleService.create(session=session, **payload.model_dump())
    return instance


@router.put(path="", response_model=PeopleRead, response_class=ORJSONResponse)
async def update_person(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description=""),
    payload: PeopleUpdate = Body(..., description="People model for update"),
):
    instance = await PeopleService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PeopleModel)
    return instance


@router.patch(path="", response_model=PeopleRead, response_class=ORJSONResponse)
async def partial_update_person(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Public ID"),
    payload: PeoplePartialUpdate = Body(
        ..., description="People model for partial update"
    ),
):
    instance = await PeopleService.update_by_id(
        session=session, id=id, **payload.model_dump()
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PeopleModel)
    return instance


@router.delete(path="", response_model=PeopleRead, response_class=ORJSONResponse)
async def delete_person(
    session: AsyncSession = Depends(get_session),
    id: int = Query(..., description="Person ID"),
):
    instance = await PeopleService.delete_by_id(
        session=session, id=id
    )
    if not instance:
        raise RecordNotFound(query_fields={"id": id}, model=PeopleModel)

    return instance
