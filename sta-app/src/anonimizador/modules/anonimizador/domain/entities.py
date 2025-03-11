from __future__ import annotations
from dataclasses import dataclass, field

import src.saludtech.modules.clients.domain.value_objects as vo
from src.saludtech.seedwork.domain.entities import SourceAggregation, Entity

@dataclass
class User(Entity) :
    username : vo.User.username = field(default_factory = vo.User.username)
    password : vo.User.password = field(default_factory = vo.User.password)

    def __str__(self) -> str :
        return self.username