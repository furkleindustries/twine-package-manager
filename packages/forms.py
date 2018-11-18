from django.forms import ModelForm

from .models import Package


class PackageCreateForm(ModelForm):
    class Meta:
        model = Package
        fields = ('name', 'description', 'homepage', 'keywords', 'tag')


class PackageUpdateForm(ModelForm):
    class Meta:
        model = Package
        fields = ('description', 'homepage', 'keywords', 'tag')
