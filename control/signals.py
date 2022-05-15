from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account, Room
import string, random

def uuid_chat():
    uuid = ''
    for i in range(0,12):
        uuid += random.choice(string.hexdigits)
    return uuid


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=Room)
def create_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uuid = uuid_chat()
        instance.save()
