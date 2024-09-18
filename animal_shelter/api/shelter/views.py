from rest_framework import viewsets, permissions
from apps.shelter.models import ShelterUser, Animal, Adoption
from .serializers import AnimalSerializer, AdoptionSerializer
from .serializers import VolunteerSerializer, AdoptantSerializer, \
                         VolunteerCreationSerializer, AdoptantCreationSerializer
from .permissions import IsAdmin, IsAdoptant, IsVolunteer, IsOwnResource
from rest_framework.permissions import IsAuthenticated, exceptions

class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = ShelterUser.objects.filter(is_volunteer=True)
    permission_classes = [IsAuthenticated, IsOwnResource]
    
    def get_queryset(self):
        if self.request.user.is_volunteer:
            return ShelterUser.objects.filter(id=self.request.user.id, is_volunteer=True)
        elif self.request.user.is_superuser:
            return ShelterUser.objects.filter(is_volunteer=True)
        return ShelterUser.objects.none()  
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VolunteerCreationSerializer
        return VolunteerSerializer
    
class AdoptantViewSet(viewsets.ModelViewSet):
    queryset = ShelterUser.objects.filter(is_adoptant=True)
    permission_classes = [IsAuthenticated, IsOwnResource]
    
    def get_queryset(self):
        # Un adoptante solo puede ver su propio perfil
        if self.request.user.is_adoptant:
            return ShelterUser.objects.filter(id=self.request.user.id, is_adoptant=True)
        # Los voluntarios pueden ver todos los adoptantes
        elif self.request.user.is_volunteer or self.request.user.is_superuser:
            return ShelterUser.objects.filter(is_adoptant=True)
        # Si no es adoptante ni voluntario, no tiene acceso
        return ShelterUser.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdoptantCreationSerializer
        return AdoptantSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    # queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]
        
    def get_queryset(self):
        if self.request.user.is_adoptant:
            return Animal.objects.filter(status=Animal.STATUS_AVAILABLE)
        elif self.request.user.is_volunteer:
            return Animal.objects.all()
        elif self.request.user.is_superuser:
            return Animal.objects.all()
        else:
            return Animal.objects.none()

    def perform_update(self, serializer):
        if self.request.user.is_volunteer or self.request.user.is_superuser:
            serializer.save()
        else:
            raise exceptions.PermissionDenied("No tienes permiso para modificar el estado del animal.")
            # raise permissions.PermissionDenied("No tienes permiso para modificar el estado del animal")
    
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT', 'PATCH']:
    #         if not (self.request.user.is_volunteer or self.request.user.is_superuser):
    #             return [permissions.Denied("No tienes permiso para modificar animales.")]
    #     return super().get_permissions()

class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all()
    serializer_class = AdoptionSerializer
    permission_classes = [IsAuthenticated]
       
    def get_queryset(self):
        if self.request.user.is_adoptant:
            return Adoption.objects.filter(adopter=self.request.user)
        elif self.request.user.is_volunteer or self.request.user.is_superuser:
            return Adoption.objects.all()
        else:
            return Adoption.objects.none()
    
    def perform_create(self, serializer):
        if self.request.user.is_adoptant:
            serializer.save(adopter=self.request.user)
        else:
            raise permissions.PermissionDenied("No tienes permiso para solicitar una adopción")

