from django.db import models
from django.contrib.auth.models import User
from re import split

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
    homepage = models.URLField(blank=True, default='')

    default_version = models.ForeignKey(
        Version,
        blank=True,
        default='',
        null=True,
        on_delete=models.SET_DEFAULT,
    )

    keywords = models.TextField(blank=True, default='')
    tag = models.TextField(blank=True, default='')

    date_created = models.DateTimeField(auto_now_add=True)

    downloads = models.IntegerField(default=0)

    def split_keywords(self):
        return split(r', *', self.keywords)

    def __str__(self):
        return self.name


class DeletedPackage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner_id = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now_add=True)
