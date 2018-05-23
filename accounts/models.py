from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField

    email_visible = models.BooleanField(default=False)

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

    create_time = models.DateTimeField(
        'date created',
        auto_now_add=True,
    )