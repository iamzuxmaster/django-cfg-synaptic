from django.db.models.signals import post_save
from django.dispatch import receiver
from control.models import Account
from .models import Moderator,Order
import random
import string



@receiver(post_save, sender=Account)
def create_moderator(sender, instance, created,**kwargs):
    if not created:
        if instance.role  == 'moderator':
            Moderator.objects.get_or_create(account=instance)


@receiver(post_save, sender=Order)
def create_uuid(sender, instance, created, **kwargs):
    if created:
        ab = 'AB'
        cde = 'CDEFGHIJKLMN'
        numbers = str(string.digits)
        code = ''
        for i in range(0, 1): 
            code += random.choice(ab)
        for i in range(0, 1):
            code += random.choice(cde)
        for i in range(0,8):
            code += random.choice(numbers)
        instance.uuid = code
        instance.save()