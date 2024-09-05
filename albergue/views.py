from rest_framework import viewsets
from .models import Voluntario, Adoptador, Animal, Adopcion
from .serializers import VoluntarioSerializer, AdoptadorSerializer, AnimalSerializer, AdopcionSerializer

class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer


class AdoptadorViewSet(viewsets.ModelViewSet):
    queryset = Adoptador.objects.all()
    serializer_class = AdoptadorSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class AdopcionViewSet(viewsets.ModelViewSet):
    queryset = Adopcion.objects.all()
    serializer_class = AdopcionSerializer