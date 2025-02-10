import random
import string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import ExistingUserProfile

@receiver(pre_save, sender=ExistingUserProfile)
def create_username_password(sender, instance, **kwargs):
    if not instance.username:
        if instance.customer:
            instance.username = instance.customer.name.lower().replace(" ", "_")

    if not instance.password:
        length = 6
        chars = string.ascii_letters + string.digits 
        instance.password = ''.join(random.choice(chars) for _ in range(length))
