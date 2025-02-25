from dataclasses import dataclass, field
from datetime import datetime
from .rules import EntityIdIsImmutable
from .exceptions import IdMustBeImmutableException
from .mixins import ValidateMixinRules
import uuid

@dataclass
class Entity :
    id : uuid.UUID = field(hash = True)
    _id : uuid.UUID = field(init = False, repr = False, hash = True)
    creation_date : datetime = field(default = datetime.now())
    update_date : datetime = field(default = datetime.now())

    @classmethod
    def next_id(self) -> uuid.UUID :
        return uuid.uuid4()

    @property
    def id(self) :
        return self._id

    @id.setter
    def id(self, id : uuid.UUID) -> None :
        if not EntityIdIsImmutable(self).is_valid() :
            raise IdMustBeImmutableException()

        self.__id = self.next_id()

@dataclass
class SourceAggregation(Entity, ValidateMixinRules) :
    ...

@dataclass
class Location(Entity) :
    def __str__(self) -> str :
        ...