from pydantic_partial import create_partial_model

from src.models.people.base import PeopleBase
from src.models.base.fields import CreatedAndUpdatedField, IdField


class PeopleCreate(PeopleBase):
    pass


class PeopleUpdate(PeopleBase):
    pass


class PeopleRead(PeopleBase, IdField, CreatedAndUpdatedField):
    pass


class _PeopleFilter(PeopleBase, IdField, CreatedAndUpdatedField):
    pass


PeoplePartialUpdate = create_partial_model(PeopleUpdate, recursive=True)
PeopleFilter = create_partial_model(_PeopleFilter, recursive=True)
