from abc import ABC, abstractmethod
from uuid import UUID
from .entities import Entity

class Repository(ABC) :
    @abstractmethod
    def find_by_id(self, uuid : UUID) -> Entity :
        ...

    @abstractmethod
    def findAll(self) -> list(Entity) :
        ...

    @abstractmethod
    def add(self, entity : Entity) :
        ...

    @abstractmethod
    def update(selfs, entity : Entity) :
        ...

    @abstractmethod
    def delete(self, entity : Entity) :
        ...

class Mapper(ABC) :
    @abstractmethod
    def get_type(self) -> type :
        ...

    @abstractmethod
    def entity_to_dto(self, entity : Entity) -> type :
        ...

    @abstractmethod
    def dto_to_entity(self, dto : any) ->  Entity :
        ...