from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Version(models.Model):
    semver_identifier = models.CharField(max_length=128)

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    description = models.TextField(blank=True, default='')
    js = models.TextField(blank=True, default='')
    css = models.TextField(blank=True, default='')

    parent_package = models.ForeignKey(
        'packages.Package',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )

    date_created = models.DateTimeField(default=timezone.now, editable=False)
