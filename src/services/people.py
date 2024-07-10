from src.models.people.model import PeopleModel
from src.services.orm.models import ModelService


class PeopleService(ModelService):
    model = PeopleModel

