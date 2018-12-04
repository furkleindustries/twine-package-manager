from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Version(models.Model):
    semver_identifier = models.CharField(max_length=128)

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False,
    )

    description = models.TextField(blank=True, default='', editable=False)
    js = models.TextField(blank=True, default='', editable=False)
    css = models.TextField(blank=True, default='', editable=False)

    parent_package = models.ForeignKey(
        'packages.Package',
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
    )

    date_created = models.DateTimeField(default=timezone.now, editable=False)

    is_default = models.BooleanField(default=False, blank=True)
