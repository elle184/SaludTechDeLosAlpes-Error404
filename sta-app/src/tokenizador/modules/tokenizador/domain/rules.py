from src.tokenizador.seedwork.domain.rules import BusinessRule
from .value_objects import User

class UserValid(BusinessRule) :
    user : User

    def __init__(self, user, message = 'Username is not valid') :
        super().__init__(message)
        self.user = user

    def is_valid(self) -> bool :
        return self.user.username
