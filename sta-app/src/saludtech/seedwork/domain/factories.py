from abc import ABC, abstractmethod
from .repositories import Mapper
from .mixins import ValidateMixinRules

class Factory(ABC, ValidateMixinRules) :
    @abstractmethod
    def create_object(self, obj : any, mapper : Mapper = None) -> any :
        ...