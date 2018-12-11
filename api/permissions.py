from rest_framework import permissions


class PackageIsOwnerOrReadOnly(permissions.BasePermission):
    ''' Custom permission to only allow owners of a package to edit it. '''
    def has_object_permission(self, request, view, package):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the package.
        return package.owner == request.user


class ProfileIsOwnerOrReadOnly(permissions.BasePermission):
    ''' Custom permission to only allow owners of a profile to edit it. '''
    def has_object_permission(self, request, view, profile):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the profile's underlying user.
        return profile.user == request.user


class VersionIsOwnerOrReadOnly(permissions.BasePermission):
    ''' Custom permission to only allow owners of a profile to edit it. '''
    def has_object_permission(self, request, view, version):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the version's
        # parent package.
        return version.parent_package.owner == request.user
