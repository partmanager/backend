import logging
from django.db.models import signals
from django.dispatch import receiver

from .models import ProjectVersion
from .models import BOM

logger = logging.getLogger('projects')


@receiver(signals.post_save, sender=ProjectVersion)
def on_project_created(sender, instance, created, **kwargs):
    if created:
        logger.info('Project version created. Creating BOM')
        obj = BOM(
            name=f"BOM For {instance.project.name} -> {instance.name}",
            project=instance
        )
        obj.save()
