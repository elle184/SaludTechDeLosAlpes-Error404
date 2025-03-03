import pulsar
from pulsar.schema import *
from sta.authentication.infrastructure.schema.v1.events import CreatedSessionPayload
import sta.seedwork.presentation.api as api

from flask import request
from sta.authentication.application.mappers import AuthenticationMapperDTOJson

bp = api.create_blueprint('authentication', '/authentication')

@bp.route("/login", methods = ('GET',))
def login_async() :
    mapper = AuthenticationMapperDTOJson()

    client = pulsar.Client('pulsar://localhost:6650')
    publisher = client.create_producer(
        'persistent://public/default/persistent/my-topic'
        , schema = AvroSchema(CreatedSessionPayload))

    return mapper.external_to_dto(request.json).username