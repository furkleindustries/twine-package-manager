from django.db.models import Count
from django.db.utils import IntegrityError

from rest_framework import filters, response

from .pagination import PageSizeAwareOffsetPagination
from .serializers import PackageSerializer, ProfileSerializer

from packages.models import Package, DeletedPackage
from profiles.models import Profile


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


class ProfileDetailMixin():
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user_id=self.kwargs['user_id'])


class IntegrityErrorAwareMixin():
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as err:
            return response.Response({
                'error': [
                    'There was an error in creating the package. It is ' +
                    'possible there is already a package by the same name ' +
                    'or ID.',
                ],
            }, status=400)


class PackageExistsOrExistedAwareMixin(IntegrityErrorAwareMixin):
    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if name:
            package = None
            try:
                package = Package.objects.get(name=name)
            except Package.DoesNotExist:
                pass

            if package:
                return response.Response({
                    'error': [
                        'There is already a package by the same name.',
                    ],
                }, status=400)

            deleted_package = None
            try:
                deleted_package = DeletedPackage.objects.get(name=name)
            except DeletedPackage.DoesNotExist:
                pass

            if deleted_package:
                return response.Response({
                    'error': [
                        'There was a package by the same name, but it was ' +
                        'deleted, and therefore cannot be used again.',
                    ],
                }, status=400)

        return super().create(request, *args, **kwargs)
