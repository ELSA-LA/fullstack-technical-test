from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from albergue.models import Usuario, Animal
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_superuser(
            email="admin@example.com",
            nombre="Admin",
            apellido="User",
            password="adminpass",
        )
        self.voluntario = Usuario.objects.create_user(
            email="voluntario@example.com",
            nombre="Volunteer",
            apellido="User",
            password="voluntariopass",
            rol=Usuario.VOLUNTARIO,
        )
        self.adoptante = Usuario.objects.create_user(
            email="adoptante@example.com",
            nombre="Adopter",
            apellido="User",
            password="adoptantepass",
            rol=Usuario.ADOPTANTE,
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.cookies['access_token'] = str(refresh.access_token)

    def test_list_users_as_admin(self):
        self.authenticate(self.admin)
        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_list_users_as_voluntario(self):
        self.authenticate(self.voluntario)
        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_user_detail(self):
        self.authenticate(self.admin)
        url = reverse('usuario-detail', args=[self.adoptante.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'adoptante@example.com')

class AnimalViewSetTest(APITestCase):
    def setUp(self):
        self.admin = Usuario.objects.create_superuser(
            email="admin@example.com",
            nombre="Admin",
            apellido="User",
            password="adminpass",
        )
        self.animal = Animal.objects.create(
            nombre="Charlie",
            edad=2,
            raza="Golden Retriever",
            tipo=Animal.Tipo.PERRO,
            estado=Animal.Estado.EN_ADOPCION,
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.cookies['access_token'] = str(refresh.access_token)

    def test_list_animals(self):
        self.authenticate(self.admin)
        url = reverse('animal-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_create_animal(self):
        self.authenticate(self.admin)
        url = reverse('animal-list')
        data = {
            'nombre': 'Rex',
            'edad': 3,
            'raza': 'German Shepherd',
            'tipo': Animal.Tipo.PERRO,
            'estado': Animal.Estado.EN_ADOPCION,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)