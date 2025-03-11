from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from tokenizador.seedwork.domain.events import (DomainEvent)

@dataclass
class TokenCreated(DomainEvent) :
    user_id : uuid.UUID = None
    token : uuid.UUID = None