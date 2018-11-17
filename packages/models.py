from re import split

from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

from versions.models import Version


def split_keywords(keywords):
    return split(r'(,\s*)|\s+', keywords)


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

    keywords = ArrayField(models.CharField(max_length=255, default=''),
                          blank=True, default=list)

    tag = models.TextField(blank=True, default='')

    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_modified = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class DeletedPackage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner_id = models.IntegerField(null=False)
    date_deleted = models.DateTimeField(default=timezone.now, editable=False)


class PackageDownload(models.Model):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
    )

    date_downloaded = models.DateTimeField(default=timezone.now,
                                           editable=False)
