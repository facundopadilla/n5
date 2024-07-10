from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class IdField(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True, description="Internal ID")


class CreatedAndUpdatedField(SQLModel):
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False, description="Created at"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        description="Updated at",
        sa_column_kwargs={
            "onupdate": lambda: datetime.utcnow()
        }
    )



class BaseSQLModel(IdField, CreatedAndUpdatedField):
    pass
