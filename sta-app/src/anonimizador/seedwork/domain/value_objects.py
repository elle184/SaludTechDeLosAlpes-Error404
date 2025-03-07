from dataclasses import dataclass
from abc import ABC

@dataclass(frozen = True)
class ValueObject :
    ...

@dataclass(frozen = True)
class User(ABC, ValueObject) :
    username : str
    password : str