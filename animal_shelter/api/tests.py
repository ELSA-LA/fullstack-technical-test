from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.shelter.models import ShelterUser, Animal, Adoption
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.shelter.models import Animal, Adoption
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class VolunteerViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='volunteer', password='password', is_volunteer=True)
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.url = reverse('volunteer-list')  # Asumiendo que el nombre de tu vista es 'volunteer-list'

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_list_volunteers(self):
        self.authenticate(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_volunteer(self):
        self.authenticate(self.superuser)
        data = {'username': 'new_volunteer', 'password': 'password', 'is_volunteer': True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_volunteer_as_non_superuser(self):
        self.authenticate(self.user)
        data = {'username': 'new_volunteer', 'password': 'password', 'is_volunteer': True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdoptantViewSetTests(APITestCase):
    def setUp(self):
        self.adoptant = User.objects.create_user(username='adoptant', password='password', is_adoptant=True)
        self.volunteer = User.objects.create_user(username='volunteer', password='password', is_volunteer=True)
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.url = reverse('adoptant-list')  # Asumiendo que el nombre de tu vista es 'adoptant-list'

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_list_adoptants(self):
        self.authenticate(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_adoptant(self):
        self.authenticate(self.superuser)
        data = {'username': 'new_adoptant', 'password': 'password', 'is_adoptant': True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_adoptant_as_non_superuser(self):
        self.authenticate(self.adoptant)
        data = {'username': 'new_adoptant', 'password': 'password', 'is_adoptant': True}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AnimalViewSetTests(APITestCase):
    def setUp(self):
        self.adoptant = User.objects.create_user(username='adoptant', password='password', is_adoptant=True)
        self.volunteer = User.objects.create_user(username='volunteer', password='password', is_volunteer=True)
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.animal = Animal.objects.create(name='Buddy', status=Animal.STATUS_AVAILABLE)
        self.url = reverse('animal-list')  # Asumiendo que el nombre de tu vista es 'animal-list'

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_list_animals(self):
        self.authenticate(self.volunteer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_animal(self):
        self.authenticate(self.volunteer)
        data = {'name': 'Charlie', 'status': Animal.STATUS_AVAILABLE}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_animal(self):
        self.authenticate(self.volunteer)
        data = {'name': 'Buddy', 'status': Animal.STATUS_ADOPTED}
        response = self.client.patch(reverse('animal-detail', args=[self.animal.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_animal_as_non_volunteer(self):
        self.authenticate(self.adoptant)
        data = {'name': 'Buddy', 'status': Animal.STATUS_ADOPTED}
        response = self.client.patch(reverse('animal-detail', args=[self.animal.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdoptionViewSetTests(APITestCase):
    def setUp(self):
        self.adoptant = User.objects.create_user(username='adoptant', password='password', is_adoptant=True)
        self.volunteer = User.objects.create_user(username='volunteer', password='password', is_volunteer=True)
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.animal = Animal.objects.create(name='Buddy', status=Animal.STATUS_AVAILABLE)
        self.adoption = Adoption.objects.create(adopter=self.adoptant, animal=self.animal, status=Adoption.SA)
        self.url = reverse('adoption-list')  # Asumiendo que el nombre de tu vista es 'adoption-list'

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_create_adoption(self):
        self.authenticate(self.adoptant)
        data = {'animal': self.animal.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_adoption_as_non_adoptant(self):
        self.authenticate(self.volunteer)
        data = {'animal': self.animal.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
