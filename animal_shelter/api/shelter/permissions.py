from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser

class IsVolunteer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.is_volunteer)

class IsAdoptant(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.is_adoptant)

class IsOwnResource(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_volunteer:
            # Los voluntarios solo pueden acceder a su propio registro
            return obj.id == request.user.id and request.user.is_volunteer
        if request.user.is_adoptant:
            # Los adoptantes solo pueden acceder a su propio registro
            return obj.id == request.user.id and request.user.is_adoptant
        if request.user.is_superuser:
            return True
        return False

    def has_permission(self, request, view):
        # Permite listar y consultar para todos los usuarios autenticados
        if request.method in ['GET']:
            return True
        
        if request.user.is_volunteer:
            # Los voluntarios no pueden crear, actualizar ni eliminar otros usuarios
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return False
            # Los voluntarios pueden ver a otros adoptantes (GET requests)
            if view.basename == 'adoptant':
                return True
        
        if request.user.is_adoptant:
            # Los adoptantes pueden ver y modificar solo su propio perfil
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return request.user.is_adoptant and view.kwargs.get('pk') == str(request.user.id)
            return True
        if request.user.is_superuser:
            return True
        
        return False
