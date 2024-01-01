from rest_framework import permissions


class AuthenticatedAndReadOnly(permissions.BasePermission):
    """
    Allows only read access for authenticated users
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS
