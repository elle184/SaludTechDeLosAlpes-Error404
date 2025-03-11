import pulsar
import json
import asyncio

def publish_and_wait_for_event(topic: str, data: dict, saga_id: str, service_url="pulsar://localhost:6650", timeout=10000):
    """
    Publica el mensaje en el topic de Pulsar y espera (de forma síncrona) la confirmación de recepción
    utilizando una suscripción única basada en el saga_id.
    """
    # Usamos una suscripción única para que nuestro consumidor reciba sólo mensajes nuevos
    subscription = f"saga_{saga_id}_subscription"
    client = pulsar.Client(service_url)
    try:
        # Se crea el consumidor con posición inicial en el último mensaje (para no procesar mensajes antiguos)
        consumer = client.subscribe(
            topic, 
            subscription_name=subscription, 
            initial_position=pulsar.InitialPosition.Latest
        )
        producer = client.create_producer(topic)
        message = json.dumps(data)
        producer.send(message.encode('utf-8'))
        
        # Espera a recibir el mensaje publicado (se asume que se recibirá en un tiempo razonable)
        msg = consumer.receive(timeout_millis=timeout)
        consumer.acknowledge(msg)
        received_data = json.loads(msg.data().decode('utf-8'))
        return received_data
    finally:
        client.close()

async def publish_event_with_confirmation(topic: str, data: dict, saga_id: str, service_url="pulsar://34.135.143.83:6650", timeout=10):
    """
    Wrapper asíncrono para la función de Pulsar que se ejecuta en un thread.
    """
    # Convertimos el timeout a milisegundos para la función sincrónica
    return await asyncio.to_thread(publish_and_wait_for_event, topic, data, saga_id, service_url, timeout * 1000)
