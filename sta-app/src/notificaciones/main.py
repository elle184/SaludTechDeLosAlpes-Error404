import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import os

def time_millis():
    return int(time.time() * 1000)

class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

class SuscripcionCreadaPayload(Record):
    id_suscripcion = String()
    id_cliente = String()
    estado = String()
    fecha_creacion = Long()

class EventoSuscripcionCreada(EventoIntegracion):
    data = SuscripcionCreadaPayload  # Corrección: data es el tipo, no una instancia

PULSAR = os.getenv('PULSAR_ADDRESS', default="localhost")

client = pulsar.Client(PULSAR)
consumer = client.subscribe('eventos-suscripcion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='sub-notificacion-eventos-suscripcion', schema=AvroSchema(EventoSuscripcionCreada))

while True:
    try:
        msg = consumer.receive()
        print('=========================================')
        if msg.value():
            print("Mensaje Recibido: '%s'" % msg.value().data)
        else:
            print("Mensaje recibido sin valor")
        print('=========================================')

        print('==== Envía correo a usuario ====')

        consumer.acknowledge(msg)

    except Exception as e:
        print(f"Error al recibir o procesar mensaje: {e}")
        # Puedes agregar más lógica de manejo de errores aquí

client.close()