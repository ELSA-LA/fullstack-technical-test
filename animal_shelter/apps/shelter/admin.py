from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShelterUser, Animal, Adoption

class ShelterUserAdmin(UserAdmin):
    model = ShelterUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_volunteer', 'is_adoptant')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_volunteer', 'is_adoptant')}),
    )

admin.site.register(ShelterUser, ShelterUserAdmin)
admin.site.register(Animal)
admin.site.register(Adoption)

