from django.contrib.auth.models import User
from django.forms import ModelForm

from profiles.models import Profile


class AccountUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'homepage', 'email_visible', 'time_style',
                  'date_style')
