from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DetalleNota

@receiver(post_save, sender=DetalleNota)
def actualizar_promedio(sender, instance, **kwargs):
    pass  # El promedio se calcula bajo demanda con el método promedio()