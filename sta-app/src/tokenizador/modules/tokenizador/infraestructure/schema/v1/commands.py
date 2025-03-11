from pulsar.schema import *
from dataclasses import dataclass, field
from tokenizador.seedwork.infrastructure.schema.v1.commands import (CommandIntegration)

class CreateTokenPayloadCommand(CommandIntegration) :
    user_id = String()
    token = String()

class CreateTokenCommand(CommandIntegration) :
    data = CreateTokenPayloadCommand()