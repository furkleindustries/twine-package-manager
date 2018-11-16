from rest_framework import serializers

from packages.models import Package, PackageDownload
from profiles.models import Profile
from versions.models import Version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'author', 'owner', 'description',
                  'default_version', 'keywords', 'tag', 'date_created',
                  'date_modified')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'description', 'homepage', 'email_visible',
                  'date_style', 'time_style')


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('id', 'version_identifier', 'author', 'description', 'js',
                  'css', 'parent_package', 'date_created')
