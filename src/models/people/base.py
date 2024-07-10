import sqlmodel
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class PeopleBase(SQLModel):
    __verbose__ = "Person"
    __tablename__ = "people"

    name: str = Field(
        default=...,
        description="Person name",
        index=False,
        unique=False,
        schema_extra={"examples": ["Facundo"]}
    )
    email: EmailStr = Field(
        default=...,
        unique=True,
        index=False,
        sa_type=sqlmodel.AutoString,
        schema_extra={"examples": ["facundo.padilla@outlook.com"]}
    )
