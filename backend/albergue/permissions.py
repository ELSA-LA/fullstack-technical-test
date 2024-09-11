from rest_framework.permissions import BasePermission
from .models import Usuario


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == Usuario.ADMIN


class IsVoluntario(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == Usuario.VOLUNTARIO


class IsAdoptante(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == Usuario.ADOPTANTE
