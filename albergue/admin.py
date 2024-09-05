from django.contrib import admin
from .models import Voluntario, Adoptador, Animal, Adopcion

admin.site.register(Voluntario)
admin.site.register(Adoptador)
admin.site.register(Animal)
admin.site.register(Adopcion)
