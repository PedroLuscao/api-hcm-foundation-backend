from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .messaging import build_event, publish_event
from .models import Branch, City, Company, Country, State


REPLICATED_MODELS = {
    Country,
    State,
    City,
    Company,
    Branch,
}


def _resource_name(instance):
    return instance.__class__.__name__.lower()


def _serialize_instance(instance):
    data = {'id': instance.pk}
    for field in instance._meta.fields:
        if field.primary_key:
            continue
        value = getattr(instance, field.attname)
        data[field.name] = value
    return data


def _publish(action, instance, data):
    event = build_event(action, _resource_name(instance), instance.pk, data)
    if event:
        publish_event(event)


@receiver(post_save)
def publish_saved_model(sender, instance, created, **kwargs):
    if sender not in REPLICATED_MODELS:
        return

    action = 'created' if created else 'updated'
    _publish(action, instance, _serialize_instance(instance))


@receiver(pre_delete)
def publish_deleted_model(sender, instance, **kwargs):
    if sender not in REPLICATED_MODELS:
        return

    _publish('deleted', instance, {})
