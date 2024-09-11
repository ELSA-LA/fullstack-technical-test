from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegistroUsuarioView,
    AnimalViewSet,
    AdopcionViewSet,
    UsuarioViewSet,
    CheckAuthView,
    LogoutView,
)

router = DefaultRouter()
router.register(r"animales", AnimalViewSet)
router.register(r"adopciones", AdopcionViewSet)
router.register(r"usuarios", UsuarioViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("registro/", RegistroUsuarioView.as_view(), name="registro"),
    path("check-auth/", CheckAuthView.as_view(), name="check-auth"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
