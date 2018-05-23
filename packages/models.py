from django.db import models
from accounts.models import Account
from versions.models import Version

class Package(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        Account,
        null=True,
        on_delete=models.SET_NULL,
        related_name='package_author_relation',
    )

    owner = models.ForeignKey(
        Account,
        null=True,
        on_delete=models.SET_NULL,
    )

    description = models.TextField
    homepage = models.TextField

    default_version = models.ForeignKey(
        Version,
        null=True,
        on_delete=models.SET_NULL,
    )

    keywords = models.TextField
    tag = models.TextField