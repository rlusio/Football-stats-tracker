from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestLoginViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('login:register')
        self.logout_url = reverse('login:logout')
        self.login_url = reverse('login:login')
        self.home_url = reverse('home')
        self.user = {
            'username': 'Testing1234',
            'password1': 'IgotTooBasicPasw...',
            'password2': 'IgotTooBasicPasw...'
        }
        self.user_short_password = {
            'username': 'Testing1234',
            'password1': 'x',
            'password2': 'x'
        }
        self.user_unmatching_password = {
            'username': 'Testing1234',
            'password1': 'x',
            'password2': 'xd'
        }

    def test_register_can_access_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/register.html')   
    
    def test_login_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')
    
    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)
    
    def test_cant_register_user_with_short_password(self):
        response = self.client.post(self.register_url, self.user_short_password, format='text/html')
        self.assertEqual(response.status_code, 400)
    
    def test_cant_register_user_with_unmatching_passwords(self):
        response = self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
        self.assertEqual(response.status_code, 400)
    
    def test_login_success(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)
        user_exists = User.objects.filter(username=self.user['username']).exists()
        self.assertTrue(user_exists)
        response = self.client.post(self.login_url, {'username': self.user['username'], 'password': self.user['password1']}, format='text/html')
        self.assertEqual(response.status_code, 302)
    
    def test_logout_post(self):
        user = User.objects.create_user(username='testuser123', password='testpassw1!')
        self.client.login(username='testuser123', password='testpassw1!')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)