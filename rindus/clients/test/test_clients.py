""""Clients test."""

# Django
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse

# Model
from rindus.clients.models import Client
from rindus.users.models import User

class ClientsTestCase(TestCase):
    """Client creation and manipulation test case."""

    def setUp(self):
        """Test case setup."""

        self.user= User.objects.create(
            first_name='Luis',
            last_name='Gonzalez',
            email='luisgonzalezb93@gmail.com',
            username='luisgb',
            password='admin123'
        )
        self.user.set_password('admin123')
        self.user.save()

        self.user2= User.objects.create(
            first_name='Pedro',
            last_name='Samino',
            email='z52gobel@uco.es',
            username='pedro',
            password='admin123'
        )
        self.user2.set_password('admin123')
        self.user2.save()
    
    def test_client_generation(self):
        """Validation in client must work."""

        client1 = Client.objects.create(
            user= self.user,
            first_name="Manuel",
            last_name="Gomez",
            iban='ES8901822886710201529235'
        )
        client1.full_clean()
        client1.iban = 'es8901822' # Not validate iban
        self.assertRaises(ValidationError, client1.full_clean)

    def test_permission_views_manipulation_creator(self):
        """Administrators should be able to create, read, update and delete users (clients)."""

        #Check our user is logged in
        login = self.client.login(username='luisgonzalezb93@gmail.com', password='admin123')
        resp = self.client.get(reverse('clients:feed'))
        self.assertEqual(str(resp.context['user']), 'luisgb')

        client2 = Client.objects.create(
            user= self.user,
            first_name="Pedro",
            last_name="Perez",
            iban='ES8389401822886710201529235'
        )

        response = self.client.get(reverse('clients:update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('clients:delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        
    def test_permission_views_manipulation_not_creator(self):
        """Restrict manipulation operations on a user (client) to the administrator who created them."""

        #Check our user is logged in
        login = self.client.login(username='z52gobel@uco.es', password='admin123')
        resp = self.client.get(reverse('clients:feed'))
        self.assertEqual(str(resp.context['user']), 'pedro')

        
        response = self.client.get(reverse('clients:update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)
        
        response = self.client.get(reverse('clients:delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)
        
