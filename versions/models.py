from django.db import models
from accounts.models import Account

class Version(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
    )

    description = models.TextField
    version_identifier = models.TextField
    js = models.TextField
    css = models.TextField
    time_created = models.DateTimeField(auto_now_add=True)