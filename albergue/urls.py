from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoluntarioViewSet, AdoptadorViewSet, AnimalViewSet, AdopcionViewSet

router = DefaultRouter()
router.register(r'voluntarios', VoluntarioViewSet)
router.register(r'adoptadores', AdoptadorViewSet)
router.register(r'animales', AnimalViewSet)
router.register(r'adopciones', AdopcionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]