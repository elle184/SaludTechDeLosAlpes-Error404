from pulsar.schema import *
from sta.seedwork.infrastructure.schema.v1.events import EventIntegration

class CreatedSessionPayload(Record) :
    username = String()
    password = String()

class CreatedSessionEvent(EventIntegration) :
    data = CreatedSessionPayload()