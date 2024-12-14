from rest_framework import permissions
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso para permitir solo a los administradores realizar cambios.
    """
    def has_permission(self, request, view):
        # Solo los admins pueden hacer POST, PUT o DELETE
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsVolunteerOrReadOnly(permissions.BasePermission):
    """
    Permiso para permitir solo a los voluntarios acceder a ciertas vistas.
    """
    def has_permission(self, request, view):
        if request.user.user_type == 'volunteer':
            return True
        return request.method in permissions.SAFE_METHODS


class IsAdminUser(permissions.BasePermission):
    """
    Permiso para permitir solo a los administradores acceder a ciertas vistas.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsVolunteerOrReadOnly(permissions.BasePermission):
    """
    Permiso para permitir a los voluntarios cambiar el estado de un animal.
    """
    def has_permission(self, request, view):
        if request.user and request.user.user_type == 'volunteer':
            return True
        return request.method in permissions.SAFE_METHODS
