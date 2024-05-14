from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import send_notification

@receiver(post_save, sender=News)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        send_notification.delay(instance.id)