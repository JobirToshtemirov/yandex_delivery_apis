from rest_framework.permissions import BasePermission, SAFE_METHODS

from app_users.models import UserRoleChoice


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.status == UserRoleChoice.ADMIN


class IsRestaurant(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoleChoice.RESTAURANT


class IsBranch(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoleChoice.BRANCH


class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoleChoice.COURIER


class IsUserOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated users to perform read-only operations.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) or if the user is authenticated
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods or if the user is the owner of the object
        return request.method in SAFE_METHODS or obj == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it,
    while allowing read-only access to others.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) or if the user is authenticated
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods or if the user is the owner of the object
        return request.method in SAFE_METHODS or obj.user == request.user