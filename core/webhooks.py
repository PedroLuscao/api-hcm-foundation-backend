import uuid
import logging
import requests
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


WEBHOOK_URL = getattr(settings, 'WEBHOOK_URL', None)
WEBHOOK_TOKEN = getattr(settings, 'WEBHOOK_TOKEN', None)

# Mapeamento do nome do model para o enum TipoEntidadeReplicacao do Java
ENTITY_MAP = {
    'user':        'USER',
    'country':     'PAIS',
    'state':       'ESTADO',
    'city':        'CITY',
    'company':     'COMPANY',
    'branch':      'BRANCH',
    'costcenter':  'COST_CENTER',
    'employee':    'EMPLOYEE',
}

# Mapeamento da ação para o enum TipoAcaoReplicacao do Java
ACTION_MAP = {
    'created': 'CREATE',
    'updated': 'UPDATE',
    'deleted': 'DELETE',
}


def _send(action: str, resource: str, source_id: str, data: dict):
    if not WEBHOOK_URL:
        return

    entity = ENTITY_MAP.get(resource)
    if not entity:
        return

    payload = {
        'eventId':   str(uuid.uuid4()),
        'entity':    entity,
        'action':    ACTION_MAP[action],
        'sourceId':  str(source_id),
        'updatedAt': datetime.now().isoformat(),
        'data':      data,
    }

    headers = {'Content-Type': 'application/json'}
    if WEBHOOK_TOKEN:
        headers['X-Webhook-Token'] = WEBHOOK_TOKEN

    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=5)
        logger.info(
            'Webhook enviado | event=%s entity=%s sourceId=%s status=%s body=%s',
            payload['eventId'], payload['entity'], payload['sourceId'],
            response.status_code, response.text
        )
    except requests.RequestException as e:
        logger.error('Webhook falhou | entity=%s action=%s erro=%s', entity, action, str(e))


class WebhookMixin:
    def get_resource_name(self):
        return self.queryset.model.__name__.lower()

    def perform_create(self, serializer):
        serializer.save()
        _send('created', self.get_resource_name(), serializer.instance.pk, dict(serializer.data))

    def perform_update(self, serializer):
        serializer.save()
        _send('updated', self.get_resource_name(), serializer.instance.pk, dict(serializer.data))

    def perform_destroy(self, instance):
        resource = self.get_resource_name()
        source_id = instance.pk
        instance.delete()
        _send('deleted', resource, source_id, {})
