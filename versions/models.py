from django.db import models
from django.contrib.auth.models import User


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
    time_created = models.DateTimeField(auto_now_add=True)

    parent_package = models.ForeignKey(
        'packages.Package',
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return '%s - %s' % (self.parent_package, self.version_identifier)