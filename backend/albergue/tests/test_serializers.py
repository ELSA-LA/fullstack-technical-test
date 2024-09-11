from django.test import TestCase
from albergue.serializers import UsuarioSerializer, AnimalSerializer
from albergue.models import Usuario, Animal

class UsuarioSerializerTest(TestCase):
    def setUp(self):
        self.user_attributes = {
            'email': 'test@example.com',
            'nombre': 'Jane',
            'apellido': 'Doe',
            'rol': Usuario.VOLUNTARIO,
            'password': 'securepassword'
        }
        self.serializer_data = {
            'email': 'newuser@example.com',
            'nombre': 'John',
            'apellido': 'Smith',
            'rol': Usuario.ADOPTANTE,
            'password': 'newpassword'
        }
        self.user = Usuario.objects.create(**self.user_attributes)
        self.serializer = UsuarioSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'email', 'nombre', 'apellido', 'rol'])

    def test_email_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['email'], self.user_attributes['email'])

class AnimalSerializerTest(TestCase):
    def setUp(self):
        self.animal_attributes = {
            'nombre': 'Charlie',
            'edad': 4,
            'raza': 'Golden Retriever',
            'tipo': Animal.Tipo.PERRO,
            'estado': Animal.Estado.EN_ADOPCION
        }
        self.animal = Animal.objects.create(**self.animal_attributes)
        self.serializer = AnimalSerializer(instance=self.animal)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'nombre', 'edad', 'raza', 'tipo', 'estado'])

    def test_nombre_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['nombre'], self.animal_attributes['nombre'])