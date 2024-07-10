from sqlmodel import SQLModel, Field


class PoliceOfficerBase(SQLModel):
    __verbose__ = "Police officer"
    __tablename__ = "police_officers"

    name: str = Field(
        default=...,
        description="Police officer",
        unique=False,
        index=False,
        schema_extra={"examples": ["Clancy Wiggum (Gorgory)"]}
    )
    badge: str = Field(
        default=...,
        description="Police badge",
        unique=True,
        index=True,
        schema_extra={"examples": ["180"]}
    )
