from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Usuario, Animal, Adopcion
from .serializers import UsuarioSerializer, AnimalSerializer, AdopcionSerializer
from .permissions import IsAdmin, IsVoluntario, IsAdoptante
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    #authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [permission() for permission in self.permission_classes]
        if self.request.user.rol == Usuario.ADMIN:
            self.permission_classes = [IsAdmin]
        elif self.request.user.rol == Usuario.VOLUNTARIO:
            self.permission_classes = [IsVoluntario]
        return super().get_permissions()


class AdopcionViewSet(viewsets.ModelViewSet):
    queryset = Adopcion.objects.all()
    serializer_class = AdopcionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [permission() for permission in self.permission_classes]

        if self.request.user.rol == Usuario.ADMIN:
            self.permission_classes = [IsAdmin]
        elif self.request.user.rol == Usuario.VOLUNTARIO:
            self.permission_classes = [IsVoluntario]
        elif self.request.user.rol == Usuario.ADOPTANTE:
            self.permission_classes = [IsAdoptante]
        return super().get_permissions()
