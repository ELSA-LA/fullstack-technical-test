from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistroUsuarioView, AnimalViewSet, AdopcionViewSet

router = DefaultRouter()
router.register(r'animales', AnimalViewSet)
router.register(r'adopciones', AdopcionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
]