from sqlmodel import SQLModel, Field
from pydantic.functional_validators import field_validator

from passlib.hash import pbkdf2_sha256 as sha256


class PasswordField(SQLModel):
    password: str = Field(
        default=...,
        nullable=False,
        description="Police officer password hashed",
        schema_extra={"examples": ["a mysterious password, boo!!!"]}
    )

    @field_validator("password")  # noqa
    @classmethod
    def hash_password(cls, v: str) -> str:
        # This will be improve with password validators :)
        return sha256.hash(v)

