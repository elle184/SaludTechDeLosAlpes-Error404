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
    dto = mapper.external_to_dto(request.json)

    client = pulsar.Client('pulsar://localhost:6650')
    publisher = client.create_producer(
        'persistent://public/default/my-topic'
        , schema = AvroSchema(CreatedSessionPayload))
    event = CreatedSessionPayload(dto.username, dto.password)
    publisher.send(event)

    consumer = client.subscribe('persistent://public/default/my-topic', 'my-subscription')
    print("🚀 Esperando eventos...")

    try:
        msg = consumer.receive()
        ## event = deserialize_avro(msg.data(), user_created_schema)
        print(f"📬 Evento recibido: {event}")
        consumer.acknowledge(msg)
    except Exception as e:
        print(f"❌ Error al procesar mensaje: {e}")
        consumer.negative_acknowledge(msg)

    client.close()

    return mapper.external_to_dto(request.json).username