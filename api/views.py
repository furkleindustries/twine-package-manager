from rest_framework import generics, permissions

from api.serializers import (
    PackageSerializer, ProfileSerializer, VersionSerializer
)

from packages.models import Package, DeletedPackage, PackageDownload
from profiles.models import Profile
from versions.models import Version

from api.permissions import (
    PackageIsOwnerOrReadOnly,
    ProfileIsOwnerOrReadOnly,
    VersionIsOwnerOrReadOnly,
)


class PackageList(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          PackageIsOwnerOrReadOnly)


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


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self, pk):
        return Profile.objects.get(user_id=pk)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          ProfileIsOwnerOrReadOnly)

    def get_object(self):
        return Profile.objects.get(user_id=self.kwargs['pk'])


class VersionList(generics.ListCreateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          VersionIsOwnerOrReadOnly)

    def get(self, request):
        for version in self.get_queryset():
            parent_package = version.parent_package
            if parent_package:
                dl = PackageDownload.objects.create(
                    package=parent_package
                )

                dl.full_clean()
                dl.save()

        return super().get(request)


class VersionDetail(generics.RetrieveDestroyAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          VersionIsOwnerOrReadOnly)

    def get(self, request, pk):
        version = self.get_object()
        parent_package = version.parent_package
        if parent_package:
            dl = PackageDownload.objects.create(
                package=parent_package
            )

            dl.full_clean()
            dl.save()

        return super().get(request)
