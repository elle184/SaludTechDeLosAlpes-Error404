import pulsar
from pulsar.schema import *

from src.tokenizador.modules.tokenizador.infraestructure.schema.v1.events import TokenCreatedEvent, TokenCreatedPayload
from src.tokenizador.modules.tokenizador.infraestructure.schema.v1.commands import CreateTokenCommand, CreateTokenPayloadCommand
from src.tokenizador.seedwork.infrastructure import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Dispatcher:
    def _publish_message(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=AvroSchema(TokenCreatedEvent))
        publicador.send(mensaje)
        cliente.close()

    def publish_event(self, evento, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del evento
        print(evento.get('User').get('token'))
        payload = TokenCreatedPayload(
            token = str(evento.get('User').get('token')),
        )
        evento_integracion = TokenCreatedEvent(data=payload)
        self._publish_message(evento_integracion, topico, AvroSchema(TokenCreatedEvent))

    def publish_command(self, comando, topico):
        # TODO Debe existir un forma de crear el Payload en Avro con base al tipo del comando
        payload = CreateTokenPayloadCommand(
            user_id = str(comando.user_id)
            , token = str(comando.token)
        )
        comando_integracion = CreateTokenCommand(data=payload)
        self._publish_message(comando_integracion, topico, AvroSchema(CreateTokenCommand))
