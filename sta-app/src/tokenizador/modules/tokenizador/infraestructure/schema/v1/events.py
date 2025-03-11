from pulsar.schema import *
from src.tokenizador.seedwork.infrastructure.schema.v1.commands import CommandIntegration

class TokenCreatedPayload(Record) :
    token: String()

class TokenCreatedEvent(CommandIntegration) :
    data = TokenCreatedPayload()