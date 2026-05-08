import json
import logging
import uuid
from datetime import datetime

import pika
from django.conf import settings

logger = logging.getLogger(__name__)


ENTITY_MAP = {
    'country': 'PAIS',
    'state': 'ESTADO',
    'city': 'CIDADE',
    'company': 'EMPRESA',
    'branch': 'FILIAL',
}

ACTION_MAP = {
    'created': 'CREATE',
    'updated': 'UPDATE',
    'deleted': 'DELETE',
}


def build_event(action: str, resource: str, source_id: str, data: dict):
    entity = ENTITY_MAP.get(resource)
    if not entity:
        return None

    return {
        'eventId': str(uuid.uuid4()),
        'entity': entity,
        'action': ACTION_MAP[action],
        'sourceId': str(source_id),
        'updatedAt': datetime.now().isoformat(),
        'data': data,
    }


def publish_event(event: dict):
    if not getattr(settings, 'RABBITMQ_ENABLED', True):
        return

    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USERNAME,
        settings.RABBITMQ_PASSWORD,
    )
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        virtual_host=settings.RABBITMQ_VHOST,
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=10,
    )
    routing_key = f"replicacao.{event['entity'].lower()}.{event['action'].lower()}"

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(
            exchange=settings.RABBITMQ_REPLICATION_EXCHANGE,
            exchange_type='topic',
            durable=True,
        )
        channel.exchange_declare(
            exchange=settings.RABBITMQ_REPLICATION_DLX,
            exchange_type='topic',
            durable=True,
        )
        channel.queue_declare(
            queue=settings.RABBITMQ_REPLICATION_QUEUE,
            durable=True,
            arguments={'x-dead-letter-exchange': settings.RABBITMQ_REPLICATION_DLX},
        )
        channel.queue_declare(
            queue=settings.RABBITMQ_REPLICATION_DLQ,
            durable=True,
        )
        channel.queue_bind(
            queue=settings.RABBITMQ_REPLICATION_QUEUE,
            exchange=settings.RABBITMQ_REPLICATION_EXCHANGE,
            routing_key=settings.RABBITMQ_REPLICATION_ROUTING_KEY,
        )
        channel.queue_bind(
            queue=settings.RABBITMQ_REPLICATION_DLQ,
            exchange=settings.RABBITMQ_REPLICATION_DLX,
            routing_key='#',
        )
        channel.basic_publish(
            exchange=settings.RABBITMQ_REPLICATION_EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(event, ensure_ascii=False),
            properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=pika.DeliveryMode.Persistent,
                message_id=event['eventId'],
            ),
            mandatory=True,
        )
        connection.close()
        logger.info(
            'Evento publicado no RabbitMQ | event=%s routingKey=%s',
            event['eventId'],
            routing_key,
        )
    except pika.exceptions.AMQPError as exception:
        logger.error(
            'Falha ao publicar no RabbitMQ | event=%s erro=%s',
            event.get('eventId'),
            str(exception),
        )
        raise
