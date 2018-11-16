from rest_framework import generics

from packages.models import Package, DeletedPackage, PackageDownload
from profiles.models import Profile
from versions.models import Version
from serializers import PackageSerializer, ProfileSerializer, VersionSerializer


class PackageList(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class PackageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = PackageSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class VersionList(generics.ListCreateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer


class VersionDetail(generics.RetrieveDestroyAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
