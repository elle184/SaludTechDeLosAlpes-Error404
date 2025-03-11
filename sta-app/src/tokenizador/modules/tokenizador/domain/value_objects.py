from __future__ import annotations

from dataclasses import dataclass, field
from src.tokenizador.seedwork.domain.value_objects import User
from datetime import datetime
from enum import Enum

@dataclass(frozen = True)
class User() :
    username : str
    password : str