from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser):
#     STATUS_CHOICES = (
#         ('active', 'Activo'),
#         ('inactive', 'Inactivo'),
#     )

#     USER_TYPE_CHOICES = (
#         ('volunteer', 'Voluntario'),
#         ('adopter', 'Adoptante'),
#         ('admin', 'Administrador'),
#     )

#     email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
#     first_name = models.CharField(max_length=30, verbose_name='Nombre')
#     last_name = models.CharField(max_length=30, verbose_name='Apellido')
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='Estado')
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['user_type']
    
#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         """Devuelve True si el usuario tiene el permiso especificado."""
#         return self.is_superuser

#     def has_module_perms(self, app_label):
#         """Devuelve True si el usuario tiene permisos para ver las apps del módulo especificado."""
#         return self.is_superuser
    
#     # groups = models.ManyToManyField(
#     #     'auth.Group',
#     #     related_name='customuser_set',
#     #     blank=True,
#     # )
#     # user_permissions = models.ManyToManyField(
#     #     'auth.Permission',
#     #     related_name='customuser_set',
#     #     blank=True,
#     # )

class ShelterUser(AbstractUser):
    is_volunteer = models.BooleanField(default=False)
    is_adoptant = models.BooleanField(default=False)

    # Cambiar los `related_name` para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='shelter_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='shelter_users',
        blank=True,
    )

# Create your models here.
class BaseDataModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Creado',
        auto_now_add=True,
        null=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name='Actualizado',
        auto_now=True,
        null=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.updated_at:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


# Animal Model
class Animal(BaseDataModel):
    TYPE_DOG = 'dog'
    TYPE_CAT = 'cat'
    STATUS_AVAILABLE = 'available'
    STATUS_ADOPTED = 'adopted'
    STATUS_IN_PROCESS = 'in_process'
    STATUS_WAITING = 'waiting'

    TYPE_CHOICES = (
        (TYPE_DOG, 'Perro'),
        (TYPE_CAT, 'Gato'),
    )

    STATUS_CHOICES = (
        (STATUS_AVAILABLE, 'Disponible'),
        (STATUS_ADOPTED, 'Adoptado'),
        (STATUS_IN_PROCESS, 'En Proceso'),
        (STATUS_WAITING, 'En Espera'),
    )
    
    name = models.CharField(
        max_length=50,
        verbose_name='Nombre',
        blank=True
    )
    age = models.PositiveIntegerField(
        verbose_name='Edad',
        blank=True,
        null=True
    )
    breed = models.CharField(
        max_length=50,
        verbose_name='Raza',
        blank=True
    )
    type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        verbose_name='Tipo',
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Estado'
    )

    def __str__(self):
        return f"{self.name or 'Sin Nombre'} ({self.get_type_display()})"

    def get_name(self):
        return self.name or "No proporcionado"

    def get_age(self):
        return self.age if self.age is not None else "No proporcionada"

    def get_breed(self):
        return self.breed or "No proporcionada"

    def get_status(self):
        return self.get_status_display()



# Adoption Model
class Adoption(BaseDataModel):
    STATUS_CHOICES = (
        ('completed', 'Finalizado'),
        ('in_process', 'En Proceso'),
    )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE,related_name='adoptions', verbose_name='Animal')
    volunteer = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, related_name='volunteer_adoptions', verbose_name='Voluntario')
    adopter = models.ForeignKey(ShelterUser, on_delete=models.CASCADE, related_name='adopted_animals', verbose_name='Adoptante')
    adoption_date = models.DateTimeField(default=timezone.now, verbose_name='Fecha')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_process', verbose_name='Estado')

    def __str__(self):
        return f"Adopción de {self.animal.name} por {self.adopter.first_name} {self.adopter.last_name}"
