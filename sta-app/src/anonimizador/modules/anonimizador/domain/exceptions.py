from src.saludtech.seedwork.domain.exceptions import FactoryException

class ObjectTypeDoesNotExistsInDomainException(FactoryException) :
    def __init__(self, message='A factory does not exists for the requested type in clients module.'):
        self.__message = message
    def __str__(self):
        return str(self.__message)