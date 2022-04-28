from django.db import models
from django.contrib.auth.models import User

class UserPasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash = models.CharField(max_length=255, null=True, blank=True)
    complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
