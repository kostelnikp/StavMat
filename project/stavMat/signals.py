from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Faktura

@receiver(post_save, sender=Faktura)
def faktura_vytvorena_signal(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=f'Nová faktúra: {instance.id}',
            message=f'Bola vytvorená nová faktúra so sumou {instance.suma}.',
            from_email='stavmat@stavmat.sk',
            recipient_list=['kostelnik.peto@gmail.com'],
        )
