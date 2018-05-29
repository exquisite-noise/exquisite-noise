from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.core import mail
from urllib.parse import urlparse


class BasicViewTests(TestCase):
    """Test view routing."""

    def setup(self):
        """Create client."""
        self.client = Client()

    # def test_home_route(self):
    #     """Route to home."""
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)

    # def test_home_route2(self):
    #     """Display home."""
    #     response = self.client.get('/')
    #     self.assertIn('Exquisite', response.content.decode('utf-8'))

    def test_login_route(self):
        """Route to login."""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_route2(self):
        """Display login."""
        response = self.client.get('/accounts/login/')
        self.assertIn('Username', response.content.decode('utf-8'))

    def test_register_route(self):
        """Route to register."""
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_route2(self):
        """Display register."""
        response = self.client.get('/accounts/register/')
        self.assertIn('Email', response.content.decode('utf-8'))

    def test_logout_route(self):
        """Route to logout."""
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_logout_route2(self):
        """Display logout."""
        response = self.client.get('/accounts/logout/')
        self.assertIn('logged out', response.content.decode('utf-8'))

    def test_activate_route(self):
        """Route to activate."""
        response = self.client.get('/accounts/activate/complete/')
        self.assertEqual(response.status_code, 200)

    def test_activate_route2(self):
        """Display activate."""
        response = self.client.get('/accounts/activate/complete/')
        self.assertIn('Activation complete', response.content.decode('utf-8'))

    def test_registered_route(self):
        """Route to registered."""
        response = self.client.get('/accounts/register/complete/')
        self.assertEqual(response.status_code, 200)

    def test_registered_route2(self):
        """Display registered."""
        response = self.client.get('/accounts/register/complete/')
        self.assertIn(
            'Registration complete', response.content.decode('utf-8'))

    # def test_get_home_page(self):
    #     """Test get homepage."""
    #     response = self.client.get(reverse_lazy('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.templates[0].name, 'generic/home.html')
    #     self.assertEqual(response.templates[1].name, 'generic/base.html')

    def test_get_registration_page(self):
        """Test registration page."""
        response = self.client.get(reverse_lazy('registration_register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'registration/registration_form.html')
        self.assertEqual(response.templates[1].name, 'generic/base.html')

    def test_register_user(self):
        """Test for user registration."""
        response = self.client.post(
            reverse_lazy('registration_register'),
            {
                'username': 'meow',
                'password1': 'pass1234',
                'password2': 'pass1234',
                'email': 'meow@meow.com'
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'registration/registration_complete.html')
        self.assertEqual(response.templates[1].name, 'generic/base.html')
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, ['meow@meow.com'])
        register_url = email.body.splitlines()[-1]
        register_url = urlparse(register_url)
        response = self.client.get(register_url.path)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username='meow', password='pass1234'))
