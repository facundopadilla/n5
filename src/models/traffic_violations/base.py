from datetime import date, datetime

from sqlmodel import Field, SQLModel


class TrafficViolationBase(SQLModel):
    __verbose__ = "Traffic violation"
    __tablename__ = "traffic_violations"

    license_plate: str = Field(
        default=...,
        description="License plate",
        index=True,
        unique=False,
        schema_extra={"examples": ["ABC123"]}
    )
    timestamp: date = Field(
        default=...,
        description="Time of violation",
        index=False,
        unique=False,
        schema_extra={"examples": [datetime.now().date()]}
    )
    comment: str = Field(
        default=...,
        description="Traffic violation comment",
        unique=False,
        index=False,
        schema_extra={"examples": ["He put some air vents on the car, it gives it speed."]},
        # https://www.youtube.com/watch?v=ej9vLgraWXk
    )

