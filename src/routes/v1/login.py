from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import pbkdf2_sha256 as sha256

from src.core.exceptions import RecordNotFound, WrongPasswordError
from src.services.police_officers import PoliceOfficerService, PoliceOfficerModel
from src.database.session import get_session
from src.security.jwt import create_access_token


class Token(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="", tags=["Login"])


@router.post("/token")
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
) -> Token:
    police_officer: PoliceOfficerModel = await PoliceOfficerService.filter(  # noqa
        session=session,
        first=True,
        badge=form_data.username,
    )
    if not police_officer:
        raise RecordNotFound(
            query_fields={"username": form_data.username},
            model=PoliceOfficerService.model
        )
    if not sha256.verify(form_data.password, police_officer.password):
        raise WrongPasswordError()

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": police_officer.badge}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
