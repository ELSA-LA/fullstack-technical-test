from django.db import models

# Create your models here.
from django.db import models

# Modelo Voluntario
class Voluntario(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'A', 'Activo'
        INACTIVO = 'I', 'Inactivo'

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    estado = models.CharField(
        max_length=1,
        choices=Estado.choices,
        default=Estado.ACTIVO,
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo Adoptador
class Adoptador(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'A', 'Activo'
        INACTIVO = 'I', 'Inactivo'

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=128)
    estado = models.CharField(
        max_length=1,
        choices=Estado.choices,
        default=Estado.ACTIVO,
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo Animal
class Animal(models.Model):
    class Tipo(models.TextChoices):
        PERRO = 'P', 'Perro'
        GATO = 'G', 'Gato'

    class Estado(models.TextChoices):
        ADOPTADO = 'AD', 'Adoptado'
        EN_ADOPCION = 'EA', 'En adopción'
        EN_ESPERA_ADOPCION = 'EE', 'En espera de adopción'

    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    raza = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=1,
        choices=Tipo.choices,
    )
    estado = models.CharField(
        max_length=2,
        choices=Estado.choices,
        default=Estado.EN_ESPERA_ADOPCION,
    )
    voluntario = models.ForeignKey(Voluntario, on_delete=models.SET_NULL, null=True, related_name='animales')

    def __str__(self):
        return self.nombre

# Modelo Adopcion
class Adopcion(models.Model):
    class Estado(models.TextChoices):
        FINALIZADO = 'F', 'Finalizado'
        EN_PROCESO = 'P', 'En proceso'

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='adopciones')
    adoptador = models.ForeignKey(Adoptador, on_delete=models.CASCADE, related_name='adopciones')
    voluntario = models.ForeignKey(Voluntario, on_delete=models.SET_NULL, null=True, related_name='adopciones')
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=1,
        choices=Estado.choices,
        default=Estado.EN_PROCESO,
    )
    fecha_devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Adopción de {self.animal.nombre} por {self.adoptador.nombre}"
