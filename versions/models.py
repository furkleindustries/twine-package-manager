from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Version(models.Model):
    version_identifier = models.CharField(max_length=255)

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
        on_delete=models.CASCADE,
        null=True,
    )

    date_created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return '{} - {}'.format(self.parent_package, self.version_identifier)
