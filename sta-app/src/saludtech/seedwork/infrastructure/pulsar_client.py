import pulsar
import json
import asyncio

def publish_and_wait_for_event(topic, data: dict, saga_id: str, service_url="pulsar://localhost:6650", timeout=30000):
    """
    Publica un mensaje en el tópico 'tokenizer_event' y espera de forma síncrona la respuesta desde el tópico 'tokenizer_send_event'.
    Se utiliza el saga_id como nombre de la suscripción para recibir solo los mensajes que correspondan a la ejecución actual.
    """
    client = pulsar.Client(service_url)
    try:
        # Publica el mensaje en el tópico 'tokenizer_event'
        producer = client.create_producer("tokenizer_event")
        message = json.dumps(data)
        producer.send(message.encode('utf-8'))
        
        # Crea el consumidor en el tópico 'tokenizer_send_event'
        consumer = client.subscribe(
            "tokenizer_send_event",
            subscription_name=saga_id,  # suscripción única basada en saga_id
            initial_position=pulsar.InitialPosition.Latest
        )
        
        # Espera a recibir el mensaje con un timeout razonable
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
