from django.db import models
from accounts.models import Account

class Profile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField
    homepage = models.TextField

    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
    )