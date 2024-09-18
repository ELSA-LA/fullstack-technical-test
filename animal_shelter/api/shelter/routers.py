from rest_framework.routers import DefaultRouter
from .views import  AnimalViewSet, AdoptionViewSet, VolunteerViewSet, AdoptantViewSet

router = DefaultRouter()
# Registra los ViewSets con nombres base únicos
router.register(r'volunteers', VolunteerViewSet, basename='volunteer')
router.register(r'adoptants', AdoptantViewSet, basename='adoptant')
router.register(r'animals', AnimalViewSet, basename='animal')
router.register(r'adoptions', AdoptionViewSet, basename='adoption')