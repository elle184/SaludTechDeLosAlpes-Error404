import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import time

class ProcesarAnonimizacion(Record):
    token = String()
    data = String()

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://pulsar:6650')
        consumidor = cliente.subscribe('eventos-procesar-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='eventos-procesar-anonimizacion', schema=AvroSchema(ProcesarAnonimizacion))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')
            time.sleep(5)
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()