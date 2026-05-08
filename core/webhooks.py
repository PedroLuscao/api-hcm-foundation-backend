import logging
import requests
from django.conf import settings
from .messaging import build_event, publish_event

logger = logging.getLogger(__name__)


WEBHOOK_URL = getattr(settings, 'WEBHOOK_URL', None)
WEBHOOK_TOKEN = getattr(settings, 'WEBHOOK_TOKEN', None)

def _send(action: str, resource: str, source_id: str, data: dict):
    payload = build_event(action, resource, source_id, data)
    if not payload:
        return

    publish_event(payload)

    if not WEBHOOK_URL:
        return

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

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
