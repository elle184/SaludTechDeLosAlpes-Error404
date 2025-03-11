from __future__ import annotations
from dataclasses import dataclass, field

import src.tokenizador.modules.tokenizador.domain.value_objects as vo
from src.tokenizador.seedwork.domain.entities import SourceAggregation, Entity

@dataclass
class User(Entity) :
    username : vo.User.username = field(default_factory = vo.User.username)
    password : vo.User.password = field(default_factory = vo.User.password)

    def __str__(self) -> str :
        return self.username