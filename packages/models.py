from django.db import models
from django.contrib.auth.models import User

from versions.models import Version


class Package(models.Model):
    name = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='package_author_relation',
    )

    owner = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
    )

    description = models.TextField(blank=True, default='')
    homepage = models.TextField(blank=True, default='')

    default_version = models.ForeignKey(
        Version,
        blank=True,
        default='',
        null=True,
        on_delete=models.SET_DEFAULT,
    )

    keywords = models.TextField(blank=True, default='')
    tag = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name
