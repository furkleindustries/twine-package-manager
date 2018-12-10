from json import dumps

from django.db.models import Count
from django.forms.models import model_to_dict

from rest_framework import filters, generics, permissions, response

from api.serializers import (
    PackageSerializer, ProfileSerializer, VersionSerializer
)

from .filters import PackageSearchFilter
from packages.models import (
    Package, DeletedPackage, PackageDownload, split_keywords
)

from profiles.models import Profile
from versions.models import Version

from .mixins import IntegrityErrorAwareMixin

from .pagination import (
    PageSizeAwareCursorPagination, PageSizeAwareOffsetPagination,
)

from .permissions import (
    PackageIsOwnerOrReadOnly, ProfileIsOwnerOrReadOnly,
    VersionIsOwnerOrReadOnly,
)


class PackageListMixin():
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    pagination_class = PageSizeAwareOffsetPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name', 'date_created', 'date_modified',
                       'downloads',)
    ordering = ('-downloads',)

    def get_queryset(self):
        return self.queryset.all().annotate(
            downloads=Count('packagedownload')
        )


class PackageListOnly(PackageListMixin, generics.ListAPIView):
    pass


class PackageList(
    PackageListMixin,
    IntegrityErrorAwareMixin,
    generics.ListCreateAPIView,
):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          PackageIsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.validated_data['owner'] = self.request.user

        super().perform_create(serializer)


class PackageSearch(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    pagination_class = PageSizeAwareOffsetPagination
    filter_backends = (PackageSearchFilter,)


class PackageKeywordList(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    pagination_class = PageSizeAwareOffsetPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name', 'date_modified', 'downloads',)
    ordering = ('-downloads',)

    def get_queryset(self):
        return self.queryset.filter(
            keywords__contains=[self.kwargs['keyword'].lower()]
        ).annotate(
            downloads=Count('packagedownload')
        )


class PackageDetailMixin():
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def get_object(self):
        field = self.kwargs['field']
        if field.isdigit():
            return Package.objects.get(id=field)
        else:
            return Package.objects.get(name=field)

    def finalize_response(self, request, response, *args, **kwargs):
        if request.method == 'GET' and request.GET.get('include_versions'):
            # Register downloads of each fetched version.
            for version in response.data['versions']:
                if version['parent_package']:
                    parent_package = None
                    try:
                        parent_package = Package.objects.get(
                            id=version['parent_package']
                        )
                    except Package.DoesNotExist:
                        pass

                    if parent_package:
                        dl = PackageDownload.objects.create(
                            package=parent_package
                        )

                        dl.full_clean()
                        dl.save()

        return super().finalize_response(request, response, *args, **kwargs)


class PackageDetailRetrieveOnly(
    PackageDetailMixin,
    generics.RetrieveAPIView,
):
    pass


class PackageDetail(
    PackageDetailMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          PackageIsOwnerOrReadOnly)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        package = self.get_object()

        updated_data = request.data.copy()

        serializer = self.get_serializer(package, data=updated_data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return response.Response(serializer.data)

    def perform_update(self, serializer):
        package = self.get_object()

        keywords = split_keywords(serializer.validated_data['keywords'][0])
        keywords = [x.lower() for x in keywords]
        serializer.validated_data['keywords'] = keywords

        default_semver_id = self.request.data.get('default_version')
        if default_semver_id:
            default_version = None
            try:
                default_version = Version.objects.get(
                    parent_package=package,
                    semver_identifier=default_semver_id,
                )
            except Version.DoesNotExist:
                pass

            if default_version:
                default_version.is_default = True
                default_version.full_clean()
                default_version.save()

                # Set all other versions to not default.
                Version.objects.filter(parent_package=package).exclude(
                    id=default_version.id
                ).update(is_default=False)

        super().perform_update(serializer)


class PackageCreateVersion(generics.CreateAPIView):
    queryset = Package.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticated,
                          PackageIsOwnerOrReadOnly)

    def get_object(self):
        field = self.kwargs['field']
        queryset = self.get_queryset()
        if field.isdigit():
            return queryset.get(id=field)
        else:
            return queryset.get(name=field)

    def perform_create(self, serializer):
        package = self.get_object()
        serializer.validated_data['parent_package'] = package

        existing_version = None
        try:
            sv_key = 'semver_identifier'
            existing_version = Version.objects.get(
                semver_identifier=serializer.validated_data[sv_key],
                parent_package=package
            )
        except Version.DoesNotExist:
            pass

        if existing_version:
            raise Exception('There is already a version for this package ' +
                            'with the same semver identifier.')

        serializer.validated_data['author'] = self.request.user
        parent_package_id = serializer.validated_data['parent_package']

        preexisting_versions = Version.objects.filter(parent_package=package)

        already_default = preexisting_versions.filter(is_default=True)

        # Set the version to default if it is the only version for the package
        # or no other versions are set to default.
        if not preexisting_versions.count() or not already_default.count():
            serializer.validated_data['is_default'] = True

        super(PackageCreateVersion, self).perform_create(serializer)


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    pagination_class = PageSizeAwareCursorPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('user_id', 'name')
    ordering = ('-user_id',)


class ProfileDetailMixin():
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user_id=self.kwargs['user_id'])


class ProfileDetailRetrieveOnly(ProfileDetailMixin, generics.RetrieveAPIView):
    pass


class ProfileDetail(ProfileDetailMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          ProfileIsOwnerOrReadOnly)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        profile = self.get_object()

        updated_data = request.data.copy()

        email = updated_data.pop('email')[0]

        serializer = self.get_serializer(profile, data=updated_data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # For some reason I don't quite understand this doesn't work if
        # performed before the serializer update.
        profile.user.email = email
        profile.user.full_clean()
        profile.user.save()

        return response.Response(serializer.data)


class VersionDetail(generics.RetrieveDestroyAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          VersionIsOwnerOrReadOnly)

    def get_object(self):
        field = self.kwargs['field']

        version = None
        if field.isdigit():
            version = self.queryset.get(id=field)
        else:
            package_id = self.request.GET.get('package_id')
            if not package_id:
                raise Exception('The package_id argument must be provided ' +
                                'if the version is being searched by semver ' +
                                'identifier.')

            version = self.queryset.get(
                semver_identifier=field, parent_package__id=package_id
            )

        return version

    def finalize_response(self, request, response, *args, **kwargs):
        if request.method == 'GET':
            # Register a download of the fetched version.
            version = response.data
            if version['parent_package']:
                parent_package = None
                try:
                    parent_package = Package.objects.get(
                        id=version['parent_package']
                    )
                except Package.DoesNotExist:
                    pass

                if parent_package:
                    dl = PackageDownload.objects.create(package=parent_package)
                    dl.full_clean()
                    dl.save()

        return super().finalize_response(request, response, *args, **kwargs)
