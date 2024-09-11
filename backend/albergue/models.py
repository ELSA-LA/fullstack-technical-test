from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Modelo de Usuario personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, password=None, rol=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, rol=rol)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, password=None):
        user = self.create_user(email, nombre, apellido, password, rol="S")
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    VOLUNTARIO = "V"
    ADOPTANTE = "A"
    ADMIN = "S"

    ROLES_CHOICES = [
        (VOLUNTARIO, "Voluntario"),
        (ADOPTANTE, "Adoptante"),
        (ADMIN, "Administrador"),
    ]

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rol = models.CharField(max_length=1, choices=ROLES_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuario_groups",  # Solución del conflicto con 'auth.User'
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuario_permissions",  # Solución del conflicto con 'auth.User'
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.get_rol_display()}"


class Animal(models.Model):
    class Tipo(models.TextChoices):
        PERRO = "P", "Perro"
        GATO = "G", "Gato"

    class Estado(models.TextChoices):
        ADOPTADO = "AD", "Adoptado"
        EN_ADOPCION = "EA", "En adopción"
        EN_ESPERA_ADOPCION = "EE", "En espera de adopción"

    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    raza = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=Tipo.choices)
    estado = models.CharField(
        max_length=2, choices=Estado.choices, default=Estado.EN_ADOPCION
    )

    def __str__(self):
        return self.nombre


# Modelo Adopcion
class Adopcion(models.Model):
    class Estado(models.TextChoices):
        FINALIZADO = "F", "Finalizado"
        EN_PROCESO = "P", "En proceso"

    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="adopciones"
    )
    adoptador = models.ForeignKey(
        "Usuario",
        on_delete=models.CASCADE,
        related_name="adopciones_adoptador",
        limit_choices_to={"rol": "A"},
    )
    voluntario = models.ForeignKey(
        "Usuario",
        on_delete=models.SET_NULL,
        null=True,
        related_name="adopciones_voluntario",
        limit_choices_to={"rol": "V"},
    )
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=1, choices=Estado.choices, default=Estado.EN_PROCESO
    )
    fecha_devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Adopción de {self.animal.nombre} por {self.adoptador.nombre}"
