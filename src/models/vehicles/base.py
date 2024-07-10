from sqlmodel import Field, SQLModel


class VehicleBase(SQLModel):
    __tablename__ = 'vehicles'

    license_plate: str = Field(
        default=...,
        description='License plate',
        index=True,
        unique=True,
        schema_extra={'examples': ['ABC123']}
    )
    # This field can be a new table...
    brand: str = Field(
        default=...,
        description='Car brand',
        index=False,
        unique=False,
        schema_extra={'examples': ['Audi', 'Fiat', 'Ford']}
    )
    color: str = Field(
        default=...,
        description='Car color',
        index=False,
        unique=False,
        schema_extra={'examples': ['Red', 'Blue', 'White']}
    )
