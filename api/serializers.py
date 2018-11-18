from re import split 

from django.contrib.auth.models import User
from rest_framework import serializers

from packages.models import Package, PackageDownload
from profiles.models import Profile
from versions.models import Version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'author', 'owner', 'description',
                  'default_version', 'keywords', 'tag', 'date_created',
                  'date_modified', 'versions', 'downloads')

    name = serializers.ReadOnlyField()

    date_created = serializers.ReadOnlyField()

    default_version = serializers.SerializerMethodField()

    def get_default_version(self, package):
        return package.default_version.version_identifier

    versions = serializers.SerializerMethodField(read_only=True)

    def get_versions(self, package):
        request = self.context['request']
        include_versions = request.GET.get('include_versions')
        if include_versions:
            include_versions = split(r'(,\s*)|\s+', include_versions)
            return [
                VersionSerializer(x).data for x in Version.objects.filter(
                    parent_package=package
                ) if x.version_identifier in include_versions or (
                    'default' in include_versions and (
                        package.default_version == x
                    )
                )
            ]

        else:
            return [x['version_identifier'] for x in Version.objects.filter(
                parent_package=package
            ).values('version_identifier')]

    downloads = serializers.SerializerMethodField(read_only=True)

    def get_downloads(self, package):
        return package.packagedownload_set.count()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user_id', 'name', 'description', 'homepage', 'email',
                  'email_visible', 'date_style', 'date_created', 'time_style',
                  'packages')

    email = serializers.SerializerMethodField()

    ''' Gets the e-mail from the underlying User object. '''
    def get_email(self, profile):
        if profile.email_visible:
            return profile.user.email

    name = serializers.SerializerMethodField(read_only=True)

    ''' Gets the username from the underlying User object. '''
    def get_name(self, profile):
        return profile.user.username

    packages = serializers.SerializerMethodField(read_only=True)

    ''' Gets the names of the owned packages. '''
    def get_packages(self, profile):
        return [x['name'] for x in Package.objects.filter(
            owner=profile.user
        ).values('name')]

    ''' Necessary because self.data cannot be accessed in save(). '''
    def to_internal_value(self, data):
        internal_value = super(ProfileSerializer, self).to_internal_value(data)
        email = data.get('email')
        internal_value.update({
            'email': email,
        })

        return internal_value

    ''' Allows us to save the e-mail to the User object. '''
    def save(self, *args, **kwargs):
        user = self.context['request'].user
        user.email = self.validated_data.get('email')
        user.full_clean()
        user.save()

        super(ProfileSerializer, self).save(*args, **kwargs)


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('id', 'version_identifier', 'author', 'description', 'js',
                  'css', 'parent_package', 'date_created')
