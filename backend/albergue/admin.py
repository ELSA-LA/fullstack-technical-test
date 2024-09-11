from django.contrib import admin
from .models import Usuario, Animal, Adopcion

# Registro del modelo Usuario en el admin
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "email", "rol", "is_active", "is_staff")
    list_filter = ("rol", "is_active", "is_staff")
    search_fields = ("nombre", "apellido", "email")
    ordering = ("email",)


# Registro del modelo Animal
@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "edad", "raza", "tipo", "estado")
    list_filter = ("tipo", "estado")
    search_fields = ("nombre", "raza")
    ordering = ("nombre",)


# Registro del modelo Adopcion
@admin.register(Adopcion)
class AdopcionAdmin(admin.ModelAdmin):
    list_display = ("animal", "adoptador", "voluntario", "fecha", "estado")
    list_filter = ("estado", "fecha")
    search_fields = ("animal__nombre", "adoptador__nombre", "voluntario__nombre")
    ordering = ("fecha",)
