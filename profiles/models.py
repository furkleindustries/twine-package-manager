from re import match

from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    description = models.TextField(blank=True, default='')
    homepage = models.URLField(blank=True, default='')

    def trimmed_homepage(self):
        _match = match(r'^(?:https?://(?:www.)*)*(.+)$', self.homepage)
        if _match and _match.group(1):
            return _match.group(1)

        return self.homepage

    email_visible = models.BooleanField(default=False)

    date_created = models.DateTimeField(default=timezone.now, editable=False)

    DAY_FIRST = 'DDMM'
    MONTH_FIRST = 'MMDD'
    DATE_STYLE_CHOICES = (
        (DAY_FIRST, 'Day first'),
        (MONTH_FIRST, 'Month first'),
    )

    date_style = models.CharField(
        choices=DATE_STYLE_CHOICES,
        default=MONTH_FIRST,
        max_length=4,
    )

    TWELVE_HOURS = '12H'
    TWENTY_FOUR_HOURS = '24H'
    TIME_STYLE_CHOICES = (
        (TWELVE_HOURS, 'Twelve hours'),
        (TWENTY_FOUR_HOURS, 'Twenty-four hours'),
    )

    time_style = models.CharField(
        choices=TIME_STYLE_CHOICES,
        default=TWELVE_HOURS,
        max_length=3,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


# These two triggers automatically create a profile when a User model is
# created.
@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
