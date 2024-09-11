from django.test import TestCase
from albergue.models import Usuario, Animal, Adopcion

class UsuarioModelTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            email="user@example.com",
            nombre="John",
            apellido="Doe",
            password="testpass123",
            rol=Usuario.ADOPTANTE,
        )

    def test_usuario_creation(self):
        self.assertEqual(self.user.email, "user@example.com")
        self.assertEqual(self.user.nombre, "John")
        self.assertEqual(self.user.apellido, "Doe")
        self.assertEqual(self.user.rol, Usuario.ADOPTANTE)

class AnimalModelTest(TestCase):
    def setUp(self):
        self.animal = Animal.objects.create(
            nombre="Bobby",
            edad=2,
            raza="Labrador",
            tipo=Animal.Tipo.PERRO,
            estado=Animal.Estado.EN_ADOPCION,
        )

    def test_animal_creation(self):
        self.assertEqual(self.animal.nombre, "Bobby")
        self.assertEqual(self.animal.edad, 2)
        self.assertEqual(self.animal.raza, "Labrador")
        self.assertEqual(self.animal.tipo, Animal.Tipo.PERRO)
        self.assertEqual(self.animal.estado, Animal.Estado.EN_ADOPCION)