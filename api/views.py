from django.db.models import Count
from django.forms.models import model_to_dict

from rest_framework import filters, generics, permissions, response

from api.serializers import (
    PackageSerializer, ProfileSerializer, VersionSerializer
)

from packages.models import Package, DeletedPackage, PackageDownload
from profiles.models import Profile
from versions.models import Version

from .pagination import (
    PageSizeAwareCursorPagination, PageSizeAwareOffsetPagination,
)

from .permissions import (
    PackageIsOwnerOrReadOnly,
    ProfileIsOwnerOrReadOnly,
    VersionIsOwnerOrReadOnly,
)


class PackageList(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          PackageIsOwnerOrReadOnly)

    pagination_class = PageSizeAwareCursorPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name')
    ordering = ('-id',)


class PackageTopDownloads(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    pagination_class = PageSizeAwareOffsetPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('downloads',)
    ordering = ('-downloads',)

    def get_queryset(self):
        return self.queryset.all().annotate(
            downloads=Count('packagedownload')
        )


class PackagesMostRecentlyModified(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    pagination_class = PageSizeAwareOffsetPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('date_modified',)
    ordering = ('-date_modified',)


class PackageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          PackageIsOwnerOrReadOnly)

    def get_object(self):
        field = self.kwargs['field']
        if field.isdigit():
            return Package.objects.get(id=field)
        else:
            return Package.objects.get(name=field)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        default_version = instance.version_set.get(
            version_identifier=request.data['default_version']
        )

        instance.default_version = default_version
        instance.save()

        updated_data = request.data.copy()
        updated_data['default_version'] = instance.default_version.id

        serializer = self.get_serializer(instance, data=updated_data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(serializer.data)

    def finalize_response(self, request, response, *args, **kwargs):
        if request.method == 'GET' and self.kwargs.get('include_versions'):
            # Register downloads of each fetched version.
            for version in response.data['results'].versions:
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


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    pagination_class = PageSizeAwareCursorPagination

    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('user_id', 'name')
    ordering = ('-user_id',)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          ProfileIsOwnerOrReadOnly)

    def get_object(self):
        return Profile.objects.get(user_id=self.kwargs['user_id'])


class VersionDetail(generics.RetrieveDestroyAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          VersionIsOwnerOrReadOnly)

    def finalize_response(self, request, response, *args, **kwargs):
        if request.method == 'GET':
            # Register a download of the fetched version.
            version = response.data['results']
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
