from .rules import BusinessRule

class DomainException(BusinessRule) : 
    ...

class InvalidUsernamePasswordException(DomainException) :
    def __init__(self, message = "Invalid username or password") :
        self.__message = message

    def __str__(self) : 
        return str(self.__message)

class IdMustBeImmutableException(DomainException) :
    def __init__(self, message = 'Identifier must be immutable') :
        self.__message = message

    def __str__(self) :
        return str(self.__message)

class BusinessRuleException(DomainException) :
    def __init__(self, message) :
        self.__message = message

    def __str__(self) :
        return str(self.__message)

class FactoryException(DomainException) :
    def __init__(self, message) :
        self.__message = message

    def __str_(self) :
        return str(self.__message)