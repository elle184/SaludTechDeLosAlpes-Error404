from .entities import User
from .rules import UserValid
from .exceptions import ObjectTypeDoesNotExistsInDomainException
from src.anonimizador.seedwork.domain.repositories import Mapper, Repository
from src.anonimizador.seedwork.domain.factories import Factory
from src.anonimizador.seedwork.domain.entities import Entity
from dataclasses import dataclass

@dataclass
class _UserFactory(Factory) :
    def create_object(self, obj: any, mapper : Mapper) -> any:
        if isinstance(obj, Entity):
            return mapper.entity_to_dto(obj)
        else:
            user : User = mapper.dto_to_entity(obj)

            self.validateRule(UserValid(user))

            return user

@dataclass
class UserFactory(Factory):
    def create_object(self, obj: any, mapper : Mapper) -> any:
        if mapper.obtener_tipo() == User.__class__:
            user_factory = _UserFactory()
            return user_factory.crear_objeto(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistsInDomainException()