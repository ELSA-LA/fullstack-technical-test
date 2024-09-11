from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Usuario, Animal, Adopcion
from .serializers import (
    UsuarioSerializer,
    AnimalSerializer,
    AdopcionSerializer,
    CustomTokenObtainPairSerializer,
)
from .permissions import IsAdmin, IsVoluntario, IsAdoptante
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .pagination import CustomPageNumberPagination
from datetime import timedelta


class LogoutView(APIView):
    def post(self, request):
        response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token", path="/", domain=None)
        response.delete_cookie("refresh_token", path="/", domain=None)
        return response


class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"authenticated": True}, status=200)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Procesar el request normalmente
        response = super().post(request, *args, **kwargs)
        tokens = response.data

        # Obtener el usuario autenticado a través del serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user_role = user.rol
        # Configurar expiraciones para las cookies
        access_token_expiration = timedelta(minutes=60)
        refresh_token_expiration = timedelta(days=1)

        # Agregar el access_token en la cookie
        response.set_cookie(
            key="access_token",
            value=tokens["access"],
            httponly=True,
            expires=access_token_expiration,
            secure=True,
            samesite="None",
        )

        # Agregar el refresh_token en la cookie
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            httponly=True,
            expires=refresh_token_expiration,
            secure=True,
            samesite="None",
        )

        # Eliminar los tokens del cuerpo de la respuesta (opcional)
        del response.data["access"]
        del response.data["refresh"]

        # Agregar el rol del usuario al cuerpo de la respuesta
        response.data["role"] = user_role

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data

        # Actualizar las cookies con el nuevo access_token
        response.set_cookie(
            key="access_token",
            value=tokens["access"],
            httponly=True,
            expires=timedelta(minutes=60),
            secure=True,
            samesite="Lax",
        )

        # Opcionalmente eliminar el access token del body
        del response.data["access"]

        return response


class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        user = self.request.user

        # Permitir acceso completo a administradores, pero excluir otros admins
        if user.rol == Usuario.ADMIN:
            self.permission_classes = [IsAdmin]

        # Permitir acceso a adoptantes solo a su propio perfil
        elif user.rol == Usuario.ADOPTANTE:
            self.permission_classes = [IsAdoptante]

        # Permitir acceso a voluntarios solo a adoptantes
        elif user.rol == Usuario.VOLUNTARIO:
            self.permission_classes = [IsVoluntario]

        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        user_ids = self.request.query_params.get("user_ids", None)
        queryset = Usuario.objects.all()

        if user_ids:
            queryset = queryset.filter(id__in=user_ids.split(","))

        if user.rol == Usuario.ADMIN:
            return queryset.exclude(rol=Usuario.ADMIN)  # Excluir administradores

        elif user.rol == Usuario.ADOPTANTE:
            return queryset.objects.filter(id=user.id)  # Solo ver su propio perfil

        elif user.rol == Usuario.VOLUNTARIO:
            return queryset.filter(
                rol=Usuario.ADOPTANTE
            )  # Voluntarios solo ven a adoptantes

        return Usuario.objects.none()

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        # Los administradores pueden ver cualquier usuario excepto otros administradores
        if user.rol == Usuario.ADMIN and instance.rol != Usuario.ADMIN:
            return super().retrieve(request, *args, **kwargs)

        # Adoptantes solo pueden ver su propio perfil
        if user.rol == Usuario.ADOPTANTE and instance.id != user.id:
            return Response(
                {"error": "No tienes permiso para ver este usuario"}, status=403
            )

        # Voluntarios solo pueden ver a los adoptantes
        if user.rol == Usuario.VOLUNTARIO and instance.rol != Usuario.ADOPTANTE:
            return Response(
                {"error": "No tienes permiso para ver este usuario"}, status=403
            )

        return super().retrieve(request, *args, **kwargs)


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [permission() for permission in self.permission_classes]
        if self.request.user.rol == Usuario.ADMIN:
            self.permission_classes = [IsAdmin]
        elif self.request.user.rol == Usuario.VOLUNTARIO:
            self.permission_classes = [IsVoluntario]
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        if request.user.rol == Usuario.ADOPTANTE:
            return Response(
                {"detail": "No tienes permiso para realizar esta acción."}, status=403
            )

        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        animal_ids = self.request.query_params.get("animal_ids", None)
        queryset = Animal.objects.all()
        if animal_ids:
            queryset = queryset.filter(id__in=animal_ids.split(","))
        return queryset


class AdopcionViewSet(viewsets.ModelViewSet):
    queryset = Adopcion.objects.all()
    serializer_class = AdopcionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

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

    def get_queryset(self):
        user = self.request.user
        estado = self.request.query_params.get("estado", None)
        animal_ids = self.request.query_params.get("animal_ids", None)
        queryset = Adopcion.objects.all()
        if estado:
            queryset = queryset.filter(estado=estado)
        if animal_ids:
            queryset = queryset.filter(animal__id__in=animal_ids.split(","))
        if user.rol == Usuario.ADOPTANTE:
            return queryset.filter(adoptador=user)
        elif user.rol in [Usuario.VOLUNTARIO, Usuario.ADMIN]:
            return queryset
        return Adopcion.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        voluntario_menos_adopciones = (
            Usuario.objects.filter(rol=Usuario.VOLUNTARIO)
            .annotate(
                num_adopciones=Count(
                    "adopciones_voluntario"
                )  # Contar las adopciones en las que el usuario es voluntario
            )
            .order_by("num_adopciones")
            .first()
        )  # Obtener el voluntario con menos adopciones

        if not voluntario_menos_adopciones:
            return Response(
                {"error": "No hay voluntarios disponibles para asignar la adopción."},
                status=400,
            )

        # Asignar la adopción al adoptante y al voluntario con menos adopciones
        if user.rol == Usuario.ADOPTANTE:
            adopcion = serializer.save(
                adoptador=user, voluntario=voluntario_menos_adopciones, estado="P"
            )  # "P" es "En proceso"
            adopcion.animal.estado = Animal.Estado.EN_ESPERA_ADOPCION
            adopcion.animal.save()
        else:
            serializer.save(voluntario=voluntario_menos_adopciones)
