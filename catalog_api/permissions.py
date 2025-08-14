# catalog_api/permissions.py

from rest_framework import permissions
from rest_framework_api_key.permissions import HasAPIKey

class HasAPIKeyForWriteOperations(permissions.BasePermission):
    """
    Custom permission to only allow write operations if a valid API Key is present.
    Read operations (GET, HEAD, OPTIONS) are allowed without an API Key.
    """
    def has_permission(self, request, view):
        # Allow read-only methods (GET, HEAD, OPTIONS) for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write methods (POST, PUT, PATCH, DELETE), require a valid API Key
        return HasAPIKey().has_permission(request, view)