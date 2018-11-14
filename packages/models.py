from re import split

from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField
from django.utils import timezone

from versions.models import Version


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


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
    homepage = models.URLField(blank=True, default='')

    default_version = models.ForeignKey(
        Version,
        blank=True,
        default='',
        null=True,
        on_delete=models.SET_DEFAULT,
    )

    keywords = JSONField(blank=True, default='')
    tag = models.TextField(blank=True, default='')

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = AutoDateTimeField()

    downloads = models.IntegerField(default=0)

    def split_keywords(self):
        return split(r', *', self.keywords)

    def __str__(self):
        return self.name


class DeletedPackage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner_id = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now_add=True)
