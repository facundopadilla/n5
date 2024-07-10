from datetime import datetime, timedelta, timezone
from typing import Union, Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_session
from src.services.police_officers import PoliceOfficerService
from src.settings.jwt import JWTSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


class TokenData(BaseModel):
    username: Union[str, None] = None


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWTSettings.JWT_PRIVATE_KEY, algorithm="HS256")
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[AsyncSession, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWTSettings.JWT_PRIVATE_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await PoliceOfficerService.filter(
        session=session,
        first=True,
        badge=token_data.username
    )
    if not user:
        raise credentials_exception
    return user
