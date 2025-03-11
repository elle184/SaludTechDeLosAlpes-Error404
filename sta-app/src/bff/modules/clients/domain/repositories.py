from abc import ABC
from src.bff.seedwork.domain.repositories import Repository

class UserRepository(Repository, ABC) :
    ...